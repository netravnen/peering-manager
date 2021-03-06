# Templating

Peering Manager comes with a built-in templating feature. This feature can be
used to generate the BGP configuration of routers to peer on Internet Exchange
points but also with direct peering sessions that can be grouped together.

!!! warning
    If you use the template feature inside each Internet Exchange, you should
    move it to templates defined per-router. The original feature per-IX will
    be removed in a near future.

## Jinja2

The templating feature is based on [Jinja2](http://jinja.pocoo.org/docs/2.9/).
Defined templates just have to follow the Jinja2 syntax and Peering Manager
will take care of everything else.

## Configuration Template

The following variables are provided to generate a configuration based on a
template:

  * `my_asn` exposing the ASN specified in the configuration (your ASN)
  * `autonomous_systems` exposing the list of
    [AutonomousSystem](objects/autonomoussystem.md) that can be found in the
    [BGPGroup](objects/bgpgroup.md) or
    [InternetExchange](objects/internetexchange.md) mentioned in other
    variables. This is useful to generate prefix lists.
  * `bgp_groups` exposing details about direct peering sessions via a list of
    [BGPGroup](objects/bgpgroup.md) objects
  * `internet_exchanges` exposing Internet Exchange peering sessions via a list
    of [InternetExchange](objects/internetexchange.md) objects
  * `routing_policies` containing the list of
    [RoutingPolicy](objects/routingpolicy.md) objects
  * `communities` containing the list of [Community](objects/community.md)
    objects

It is possible to iterate over these variables, except the first one, using the
`for` keyword of Jinja2. More details can be found about how to use these in
the examples below.

### Functions And Filters

Peering Manager exposes custom functions and filters that can be used in Jinja2
based templates.

`prefix_list` will fetch the list of prefixes given two parameters: an
Autonomous System number and an address family (IP version). The ASN must be a
valid integer (e.g. 201281), the address family must be an integer as well (4
means IPv4, 6 means IPv6, any other values means both families). Here is an
example that could be used in a template for JUNOS:

```no-highlight
policy-options {
    {%- for autonomous_system in autonomous_systems %}
    {%- set asn = autonomous_system['asn'] %}
    prefix-list ipv6-as{{ asn }} {
        {%- for p in asn|prefix_list(6) %}
        {{ p.prefix }};
        {%- endfor %}
    }
    prefix-list ipv4-as{{ asn }} {
        {%- for p in asn|prefix_list(4) %}
        {{ p.prefix }};
        {%- endfor %}
    }
    {%- endfor %}
}
```

## Example

Template examples are provided for:

  * [Juniper JUNOS](juniper-junos.md)
  * [Cisco IOS-XR](cisco-iosxr.md)
  * [Arista EOS](arista-eos.md)
