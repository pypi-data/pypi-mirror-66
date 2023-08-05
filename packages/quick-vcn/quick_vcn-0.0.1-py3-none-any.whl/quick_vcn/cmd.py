import argcomplete
import argparse
import json
import logging
import oci
import os.path
import sys

LOG = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="~/.oci/config")
    parser.add_argument("--profile", default=os.getenv("OCI_CLI_PROFILE", default="DEFAULT"))
    parser.add_argument("--region")
    parser.add_argument("--compartment", required=True)

    parser.add_argument("--vcn-name", default="net")
    parser.add_argument("--vcn-cidr", default="10.0.0.0/16")

    parser.add_argument("--internet-gateway-name", default="ig")

    parser.add_argument("--subnet-name", default="sub")
    parser.add_argument("--subnet-cidr", default="10.0.0.0/24")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    conf = oci.config.from_file(os.path.expanduser(args.config), profile_name=args.profile)
    if args.region is not None:
        conf["region"] = args.region

    iam_client = oci.identity.IdentityClient(conf)
    vcn_client = oci.core.VirtualNetworkClient(conf)

    compartments = load_all(iam_client.list_compartments, conf["tenancy"], compartment_id_in_subtree=True)
    compartment = [c for c in compartments if c.name == args.compartment][0]

    LOG.info("compartment: %s", compartment.id)

    vcns = [v for v in load_all(vcn_client.list_vcns, compartment.id) if v.display_name == args.vcn_name]
    if len(vcns) == 0:
        LOG.info("creating vcn")
        vcn = vcn_client.create_vcn(oci.core.models.CreateVcnDetails(
            compartment_id=compartment.id,
            display_name=args.vcn_name,
            cidr_block=args.vcn_cidr,
            dns_label=args.vcn_name,
        )).data
    elif len(vcns) == 1:
        vcn = vcns[0]
    else:
        raise ValueError("More than one vcn found with that name")

    LOG.info("vcn: %s", vcn.id)

    # Internet gateway
    igs = [ig for ig in load_all(vcn_client.list_internet_gateways, compartment.id, vcn.id) if ig.display_name == args.internet_gateway_name]
    if len(igs) == 0:
        LOG.info("creating internet gateway")
        ig = vcn_client.create_internet_gateway(oci.core.models.CreateInternetGatewayDetails(
            compartment_id=compartment.id,
            vcn_id=vcn.id,
            display_name=args.internet_gateway_name,
            is_enabled=True,
        )).data
    elif len(igs) == 1:
        ig = igs[0]
    else:
        raise ValueError("More than one internet gateway located")

    LOG.info("internet-gateway: %s", ig.id)

    # Route table
    rt = vcn_client.get_route_table(vcn.default_route_table_id).data
    rules = rt.route_rules

    for rr in rules:
        if rr.network_entity_id == ig.id:
            LOG.debug("route table entry located for internet gateway")
            break
    else:
        LOG.info("Adding route-table entry for internet gateway")
        rules.append(oci.core.models.RouteRule(
            cidr_block="0.0.0.0/0",
            destination="0.0.0.0/0",
            destination_type="CIDR_BLOCK",
            network_entity_id=ig.id,
        ))
        vcn_client.update_route_table(rt.id, oci.core.models.UpdateRouteTableDetails(
            route_rules=rules
        ))
        rt = vcn_client.get_route_table(vcn.default_route_table_id).data

    # Subnet
    sns = [sn
           for sn in load_all(vcn_client.list_subnets, compartment.id, vcn.id)
           if sn.display_name == args.subnet_name or sn.cidr_block == args.subnet_cidr]
    if len(sns) == 0:
        LOG.info("creating subnet")
        sn = vcn_client.create_subnet(oci.core.models.CreateSubnetDetails(
            compartment_id=compartment.id,
            vcn_id=vcn.id,
            availability_domain=None,

            cidr_block=args.subnet_cidr,
            display_name=args.subnet_name,

            dns_label=args.subnet_name,
            dhcp_options_id=vcn.default_dhcp_options_id,
            prohibit_public_ip_on_vnic=False,
            route_table_id=vcn.default_route_table_id,
            security_list_ids=[vcn.default_security_list_id],
        )).data
    elif len(sns) == 1:
        sn = sns[0]
    else:
        raise ValueError("found more than one matching subnet")

    json.dump({"compartment": compartment.id, "vcn": vcn.id, "subnet": sn.id}, sys.stdout)


def load_all(call, *args, **kwargs):
    results = []
    next_page = None
    while True:
        vs = call(*args, limit=200, page=next_page, **kwargs)
        results.extend(vs.data)
        if (next_page := vs.next_page) is None:
            return results


if __name__ == '__main__':
    main()
