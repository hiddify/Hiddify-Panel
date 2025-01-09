from enum import auto, Enum
from typing import Union

from strenum import StrEnum
from fast_enum import FastEnum


class HEnum(StrEnum):
    @classmethod
    def from_str(cls, key: str) -> 'HEnum':
        return cls[key]


class Lang(HEnum):
    en = auto()
    fa = auto()
    ru = auto()
    pt = auto()
    zh = auto()
    my = auto()


class PanelMode(HEnum):
    standalone = auto()
    parent = auto()
    child = auto()


class LogLevel(HEnum):
    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    SUCCESS = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class ConfigCategory(StrEnum):
    admin = auto()
    branding = auto()
    general = auto()
    proxies = auto()
    domain_fronting = auto()
    telegram = auto()
    http = auto()
    tls = auto()
    mux = auto()
    tls_trick = auto()
    ssh = auto()
    ssfaketls = auto()
    shadowtls = auto()
    restls = auto()
    tuic = auto()
    hysteria = auto()
    ssr = auto()
    kcp = auto()
    hidden = auto()
    advanced = auto()
    too_advanced = auto()
    warp = auto()
    reality = auto()
    wireguard = auto()
    shadowsocks = auto()


class ApplyMode(StrEnum):
    apply_config = auto()
    reinstall = auto()
    nothing = auto()


def _BoolConfigDscr(category: ConfigCategory, apply_mode: ApplyMode = ApplyMode.nothing, show_in_parent: bool = True, hide_in_virtual_child=False) -> "ConfigEnum":
    return category, apply_mode, bool, show_in_parent


def _StrConfigDscr(category: ConfigCategory, apply_mode: ApplyMode = ApplyMode.nothing, show_in_parent: bool = True, hide_in_virtual_child=False) -> "ConfigEnum":
    return category, apply_mode, str, show_in_parent


def _IntConfigDscr(category: ConfigCategory, apply_mode: ApplyMode = ApplyMode.nothing, show_in_parent: bool = True, hide_in_virtual_child=False) -> "ConfigEnum":
    return category, apply_mode, int, show_in_parent


def _TypedConfigDscr(ctype: type, category: ConfigCategory, apply_mode: ApplyMode = ApplyMode.nothing, show_in_parent: bool = True, hide_in_virtual_child=False) -> "ConfigEnum":
    return category, apply_mode, ctype, show_in_parent


class ConfigEnum(metaclass=FastEnum):
    # category: ConfigCategory
    __slots__ = ('name', 'value', 'category', 'apply_mode', 'type', 'show_in_parent', 'hide_in_virtual_child')

    def __init__(self, category: ConfigCategory, apply_mode: ApplyMode = ApplyMode.apply_config, ctype=type, show_in_parent: bool = True, hide_in_virtual_child=False, name=auto):
        self.value = name
        self.name = name
        self.category = category
        self.apply_mode = apply_mode
        self.type = ctype
        self.show_in_parent = show_in_parent
        self.hide_in_virtual_child = hide_in_virtual_child

    @classmethod
    def dbvalues(cls):
        return {c.name: c for c in ConfigEnum}
    create_easysetup_link = _BoolConfigDscr(ConfigCategory.hidden, ApplyMode.nothing, hide_in_virtual_child=True)
    wireguard_enable = _BoolConfigDscr(ConfigCategory.wireguard, ApplyMode.reinstall, hide_in_virtual_child=True)
    wireguard_port = _StrConfigDscr(ConfigCategory.wireguard, ApplyMode.apply_config, hide_in_virtual_child=True)
    wireguard_ipv6 = _StrConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config, hide_in_virtual_child=True)
    wireguard_ipv4 = _StrConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config, hide_in_virtual_child=True)
    wireguard_private_key = _StrConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config, hide_in_virtual_child=True)
    wireguard_public_key = _StrConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config, hide_in_virtual_child=True)
    wireguard_noise_trick = _StrConfigDscr(ConfigCategory.wireguard, ApplyMode.apply_config)

    ssh_server_redis_url = _StrConfigDscr(ConfigCategory.hidden, hide_in_virtual_child=True)
    ssh_server_port = _StrConfigDscr(ConfigCategory.ssh, ApplyMode.apply_config, hide_in_virtual_child=True)
    ssh_server_enable = _BoolConfigDscr(ConfigCategory.ssh, ApplyMode.reinstall)
    first_setup = _BoolConfigDscr(ConfigCategory.hidden)
    core_type = _StrConfigDscr(ConfigCategory.advanced, ApplyMode.reinstall, hide_in_virtual_child=True)
    warp_enable = _BoolConfigDscr(ConfigCategory.hidden, ApplyMode.reinstall, hide_in_virtual_child=True)
    warp_mode = _StrConfigDscr(ConfigCategory.warp, ApplyMode.apply_config, hide_in_virtual_child=True)
    warp_plus_code = _StrConfigDscr(ConfigCategory.warp, ApplyMode.apply_config, hide_in_virtual_child=True)
    warp_sites = _StrConfigDscr(ConfigCategory.warp, ApplyMode.apply_config, hide_in_virtual_child=True)
    dns_server = _StrConfigDscr(ConfigCategory.general, ApplyMode.apply_config, hide_in_virtual_child=True)
    reality_fallback_domain = _StrConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config)  # removed
    reality_server_names = _StrConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config)  # removed
    reality_short_ids = _StrConfigDscr(ConfigCategory.reality, ApplyMode.apply_config, hide_in_virtual_child=True)
    reality_private_key = _StrConfigDscr(ConfigCategory.reality, ApplyMode.apply_config, hide_in_virtual_child=True)
    reality_public_key = _StrConfigDscr(ConfigCategory.reality, ApplyMode.apply_config, hide_in_virtual_child=True)
    reality_port = _StrConfigDscr(ConfigCategory.reality, ApplyMode.apply_config, hide_in_virtual_child=True)

    restls1_2_domain = _StrConfigDscr(ConfigCategory.hidden)
    restls1_3_domain = _StrConfigDscr(ConfigCategory.hidden)
    show_usage_in_sublink = _BoolConfigDscr(ConfigCategory.general)
    cloudflare = _StrConfigDscr(ConfigCategory.too_advanced)
    license = _StrConfigDscr(ConfigCategory.hidden)
    country = _StrConfigDscr(ConfigCategory.general, ApplyMode.reinstall, hide_in_virtual_child=True)
    package_mode = _StrConfigDscr(ConfigCategory.advanced, hide_in_virtual_child=True)
    utls = _StrConfigDscr(ConfigCategory.advanced)
    telegram_bot_token = _StrConfigDscr(ConfigCategory.telegram, hide_in_virtual_child=True)

    # region child-parent
    # deprecated
    is_parent = _BoolConfigDscr(ConfigCategory.hidden)
    # parent panel domain
    parent_panel = _StrConfigDscr(ConfigCategory.hidden)  # should be able to change by user
    parent_domain = _StrConfigDscr(ConfigCategory.hidden)
    parent_admin_proxy_path = _StrConfigDscr(ConfigCategory.hidden)

    # the panel mode could be one of these: "parent", "child", "standalone"
    # this config value would be 'standalone' by default. and would be set by panel itself
    panel_mode = _TypedConfigDscr(PanelMode, ConfigCategory.hidden, hide_in_virtual_child=True)
    # endregion

    log_level = _TypedConfigDscr(LogLevel, ConfigCategory.hidden, ApplyMode.reinstall, hide_in_virtual_child=True)

    unique_id = _StrConfigDscr(ConfigCategory.hidden)
    last_hash = _StrConfigDscr(ConfigCategory.hidden)
    cdn_forced_host = _StrConfigDscr(ConfigCategory.hidden)  # removed
    lang = _TypedConfigDscr(Lang, ConfigCategory.branding)
    admin_lang = _TypedConfigDscr(Lang, ConfigCategory.admin)
    admin_secret = _StrConfigDscr(ConfigCategory.hidden)  # removed

    # tls
    tls_ports = _StrConfigDscr(ConfigCategory.tls, ApplyMode.apply_config)

    tls_fragment_enable = _BoolConfigDscr(ConfigCategory.tls_trick)
    tls_fragment_size = _StrConfigDscr(ConfigCategory.tls_trick)
    tls_fragment_sleep = _StrConfigDscr(ConfigCategory.tls_trick)
    tls_mixed_case = _BoolConfigDscr(ConfigCategory.tls_trick)
    tls_padding_enable = _BoolConfigDscr(ConfigCategory.tls_trick, ApplyMode.apply_config)
    tls_padding_length = _StrConfigDscr(ConfigCategory.tls_trick, ApplyMode.apply_config)

    # mux
    mux_enable = _BoolConfigDscr(ConfigCategory.mux, ApplyMode.apply_config)
    mux_protocol = _StrConfigDscr(ConfigCategory.mux, ApplyMode.apply_config)
    mux_max_connections = _IntConfigDscr(ConfigCategory.mux, ApplyMode.apply_config)
    mux_min_streams = _IntConfigDscr(ConfigCategory.mux, ApplyMode.apply_config)
    mux_max_streams = _IntConfigDscr(ConfigCategory.mux, ApplyMode.apply_config)
    mux_padding_enable = _BoolConfigDscr(ConfigCategory.mux, ApplyMode.apply_config)
    mux_brutal_enable = _BoolConfigDscr(ConfigCategory.mux, ApplyMode.apply_config)
    mux_brutal_up_mbps = _IntConfigDscr(ConfigCategory.mux, ApplyMode.apply_config)
    mux_brutal_down_mbps = _IntConfigDscr(ConfigCategory.mux, ApplyMode.apply_config)

    http_ports = _StrConfigDscr(ConfigCategory.http, ApplyMode.apply_config)
    kcp_ports = _StrConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config)
    kcp_enable = _BoolConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config)
    decoy_domain = _StrConfigDscr(ConfigCategory.general, ApplyMode.apply_config, hide_in_virtual_child=True)
    # will be deprecated
    proxy_path = _StrConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config, hide_in_virtual_child=True)
    proxy_path_admin = _StrConfigDscr(ConfigCategory.too_advanced, ApplyMode.apply_config, hide_in_virtual_child=True)
    proxy_path_client = _StrConfigDscr(ConfigCategory.too_advanced, ApplyMode.apply_config, hide_in_virtual_child=True)
    firewall = _BoolConfigDscr(ConfigCategory.general, ApplyMode.apply_config, hide_in_virtual_child=True)
    netdata = _BoolConfigDscr(ConfigCategory.hidden, ApplyMode.reinstall)  # removed
    http_proxy_enable = _BoolConfigDscr(ConfigCategory.http)
    block_iran_sites = _BoolConfigDscr(ConfigCategory.proxies, ApplyMode.apply_config, hide_in_virtual_child=True)
    allow_invalid_sni = _BoolConfigDscr(ConfigCategory.tls, ApplyMode.apply_config, hide_in_virtual_child=True)
    auto_update = _BoolConfigDscr(ConfigCategory.general, ApplyMode.apply_config, True, hide_in_virtual_child=True)
    speed_test = _BoolConfigDscr(ConfigCategory.general, ApplyMode.reinstall, hide_in_virtual_child=True)
    only_ipv4 = _BoolConfigDscr(ConfigCategory.general, ApplyMode.apply_config, hide_in_virtual_child=True)

    shared_secret = _StrConfigDscr(ConfigCategory.proxies, ApplyMode.apply_config, hide_in_virtual_child=True)

    telegram_enable = _BoolConfigDscr(ConfigCategory.telegram, ApplyMode.reinstall)
    # telegram_secret=auto()
    telegram_adtag = _StrConfigDscr(ConfigCategory.telegram, ApplyMode.reinstall, hide_in_virtual_child=True)
    telegram_lib = _StrConfigDscr(ConfigCategory.telegram, ApplyMode.reinstall, hide_in_virtual_child=True)
    telegram_fakedomain = _StrConfigDscr(ConfigCategory.telegram, ApplyMode.reinstall, hide_in_virtual_child=True)

    v2ray_enable = _BoolConfigDscr(ConfigCategory.hidden, ApplyMode.reinstall)
    torrent_block = _BoolConfigDscr(ConfigCategory.general, ApplyMode.apply_config)

    tuic_enable = _BoolConfigDscr(ConfigCategory.tuic, ApplyMode.apply_config)
    tuic_port = _StrConfigDscr(ConfigCategory.tuic, ApplyMode.apply_config, hide_in_virtual_child=True)

    # the hysteria is refereing to hysteria2
    hysteria_enable = _BoolConfigDscr(ConfigCategory.hysteria, ApplyMode.apply_config)
    hysteria_port = _StrConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config, hide_in_virtual_child=True)
    # if be enable hysteria2 will be use salamander as obfs
    hysteria_obfs_enable = _BoolConfigDscr(ConfigCategory.hysteria, ApplyMode.apply_config)
    hysteria_up_mbps = _StrConfigDscr(ConfigCategory.hysteria, ApplyMode.apply_config)
    hysteria_down_mbps = _StrConfigDscr(ConfigCategory.hysteria, ApplyMode.apply_config)

    shadowsocks2022_enable = _BoolConfigDscr(ConfigCategory.shadowsocks, ApplyMode.apply_config)
    shadowsocks2022_method = _StrConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config)
    shadowsocks2022_port = _StrConfigDscr(ConfigCategory.shadowsocks, ApplyMode.apply_config)
    ssfaketls_enable = _BoolConfigDscr(ConfigCategory.shadowsocks, ApplyMode.reinstall)
    ssfaketls_fakedomain = _StrConfigDscr(ConfigCategory.shadowsocks, ApplyMode.apply_config, hide_in_virtual_child=True)
    shadowtls_enable = _BoolConfigDscr(ConfigCategory.shadowsocks, ApplyMode.apply_config)
    shadowtls_fakedomain = _StrConfigDscr(ConfigCategory.shadowsocks, ApplyMode.apply_config, hide_in_virtual_child=True)

    ssr_enable = _BoolConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config)
    # ssr_secret="ssr_secret"
    ssr_fakedomain = _StrConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config)

    vmess_enable = _BoolConfigDscr(ConfigCategory.proxies, ApplyMode.apply_config)
    domain_fronting_domain = _StrConfigDscr(ConfigCategory.hidden)  # removed
    domain_fronting_http_enable = _BoolConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config)  # removed
    domain_fronting_tls_enable = _BoolConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config)  # removed

    ws_enable = _BoolConfigDscr(ConfigCategory.proxies, ApplyMode.apply_config)
    grpc_enable = _BoolConfigDscr(ConfigCategory.proxies, ApplyMode.apply_config)
    httpupgrade_enable = _BoolConfigDscr(ConfigCategory.proxies, ApplyMode.apply_config)
    xhttp_enable = _BoolConfigDscr(ConfigCategory.proxies, ApplyMode.apply_config)

    vless_enable = _BoolConfigDscr(ConfigCategory.proxies, ApplyMode.apply_config)
    trojan_enable = _BoolConfigDscr(ConfigCategory.proxies, ApplyMode.apply_config)
    reality_enable = _BoolConfigDscr(ConfigCategory.proxies, ApplyMode.apply_config)
    tcp_enable = _BoolConfigDscr(ConfigCategory.proxies, ApplyMode.apply_config)
    quic_enable = _BoolConfigDscr(ConfigCategory.proxies, ApplyMode.apply_config)
    xtls_enable = _BoolConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config)
    h2_enable = _BoolConfigDscr(ConfigCategory.proxies, ApplyMode.apply_config)

    db_version = _StrConfigDscr(ConfigCategory.hidden)
    last_priodic_usage_check = _IntConfigDscr(ConfigCategory.hidden)

    branding_title = _StrConfigDscr(ConfigCategory.branding)
    branding_site = _StrConfigDscr(ConfigCategory.branding)
    branding_freetext = _StrConfigDscr(ConfigCategory.branding)
    not_found = _StrConfigDscr(ConfigCategory.hidden)
    path_vmess = _StrConfigDscr(ConfigCategory.too_advanced, ApplyMode.apply_config, hide_in_virtual_child=True)
    path_vless = _StrConfigDscr(ConfigCategory.too_advanced, ApplyMode.apply_config, hide_in_virtual_child=True)
    path_trojan = _StrConfigDscr(ConfigCategory.too_advanced, ApplyMode.apply_config, hide_in_virtual_child=True)
    path_v2ray = _StrConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config, hide_in_virtual_child=True)  # deprecated
    path_ss = _StrConfigDscr(ConfigCategory.hidden, ApplyMode.apply_config, hide_in_virtual_child=True)

    path_xhttp = _StrConfigDscr(ConfigCategory.too_advanced, ApplyMode.apply_config, hide_in_virtual_child=True)
    path_httpupgrade = _StrConfigDscr(ConfigCategory.too_advanced, ApplyMode.apply_config, hide_in_virtual_child=True)
    path_ws = _StrConfigDscr(ConfigCategory.too_advanced, ApplyMode.apply_config, hide_in_virtual_child=True)
    path_tcp = _StrConfigDscr(ConfigCategory.too_advanced, ApplyMode.apply_config, hide_in_virtual_child=True)
    path_grpc = _StrConfigDscr(ConfigCategory.too_advanced, ApplyMode.apply_config, hide_in_virtual_child=True)

    # subs
    sub_full_singbox_enable = _BoolConfigDscr(ConfigCategory.hidden)
    sub_singbox_ssh_enable = _BoolConfigDscr(ConfigCategory.hidden)
    sub_full_xray_json_enable = _BoolConfigDscr(ConfigCategory.proxies)
    sub_full_links_enable = _BoolConfigDscr(ConfigCategory.hidden)
    sub_full_links_b64_enable = _BoolConfigDscr(ConfigCategory.hidden)
    sub_full_clash_enable = _BoolConfigDscr(ConfigCategory.hidden)
    sub_full_clash_meta_enable = _BoolConfigDscr(ConfigCategory.hidden)


    #ssh host keys
    ssh_host_rsa_pk = _StrConfigDscr(ConfigCategory.hidden)
    ssh_host_rsa_pub = _StrConfigDscr(ConfigCategory.hidden)
    ssh_host_ed25519_pk = _StrConfigDscr(ConfigCategory.hidden)
    ssh_host_ed25519_pub = _StrConfigDscr(ConfigCategory.hidden)
    ssh_host_ecdsa_pk = _StrConfigDscr(ConfigCategory.hidden)
    ssh_host_ecdsa_pub = _StrConfigDscr(ConfigCategory.hidden)
    ssh_host_dsa_pk = _StrConfigDscr(ConfigCategory.hidden)
    ssh_host_dsa_pub = _StrConfigDscr(ConfigCategory.hidden)
    
    

    hiddifycli_enable = _BoolConfigDscr(ConfigCategory.hidden, ApplyMode.reinstall)

    @classmethod
    def __missing__(cls, value):
        return ConfigEnum.not_found

    def __contains__(self, other):
        return other in self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return f'{self}' == f'{other}'

    def __neg__(self, other):
        return not self.__eq__(other)

    def endswith(self, other):
        return self.name.endswith(other)  # type: ignore

    def startswith(self, other):
        return self.name.startswith(other)  # type: ignore
