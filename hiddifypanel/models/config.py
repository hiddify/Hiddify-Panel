from sqlalchemy_serializer import SerializerMixin

from hiddifypanel import Events, hutils
from hiddifypanel.cache import cache
from hiddifypanel.panel.database import db
from hiddifypanel.hutils.utils import error
from .config_enum import ConfigEnum
from flask import g


class BoolConfig(db.Model, SerializerMixin):
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True, default=0)
    # category = db.Column(db.String(128), primary_key=True)
    key = db.Column(db.Enum(ConfigEnum, values_callable=ConfigEnum.dbvalues), primary_key=True)
    value = db.Column(db.Boolean)

    def to_dict(d):
        return {
            'key': d.key,
            'value': d.value,
            'child_unique_id': d.child.unique_id if d.child else ''
        }


class StrConfig(db.Model, SerializerMixin):
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True, default=0)
    # category = db.Column(db.String(128), primary_key=True)
    key = db.Column(db.Enum(ConfigEnum, values_callable=ConfigEnum.dbvalues), primary_key=True, default=ConfigEnum.admin_secret)
    value = db.Column(db.String(2048))

    def to_dict(d):
        return {
            'key': d.key,
            'value': d.value,
            'child_unique_id': d.child.unique_id if d.child else ''
        }


@cache.cache(ttl=500)
def hconfig(key: ConfigEnum, child_id: int = None) -> str | int | None:
    if child_id == None:
        child_id = hutils.current_child_id()

    value = None
    try:
        str_conf = StrConfig.query.filter(StrConfig.key == key, StrConfig.child_id == child_id).first()
        if str_conf:
            value = str_conf.value
        else:
            bool_conf = BoolConfig.query.filter(BoolConfig.key == key, BoolConfig.child_id == child_id).first()
            if bool_conf:
                value = bool_conf.value
            else:
                # if key == ConfigEnum.ssfaketls_fakedomain:
                #     return hdomain(DomainType.ss_faketls)
                # if key == ConfigEnum.telegram_fakedomain:
                #     return hdomain(DomainType.telegram_faketls)
                # if key == ConfigEnum.fake_cdn_domain:
                #     return hdomain(DomainType.fake_cdn)
                error(f'{key} not found ')
    except:
        error(f'{key} error!')
        raise

    return value


def set_hconfig(key: ConfigEnum, value: str | bool, child_id: int = None, commit: bool = True):
    if child_id == None:
        child_id = hutils.current_child_id()
    # hconfig.invalidate(key, child_id)
    # get_hconfigs.invalidate(child_id)
    hconfig.invalidate(key, child_id)
    hconfig.invalidate(key, child_id=child_id)
    hconfig.invalidate(key=key, child_id=child_id)
    if child_id == hutils.current_child_id():
        hconfig.invalidate(key)
    # hconfig.invalidate_all()
    get_hconfigs.invalidate_all()
    old_v = None
    if key.type() == bool:
        dbconf = BoolConfig.query.filter(BoolConfig.key == key, BoolConfig.child_id == child_id).first()
        if not dbconf:
            dbconf = BoolConfig(key=key, value=value, child_id=child_id)
            db.session.add(dbconf)
        else:
            old_v = dbconf.value
    else:
        dbconf = StrConfig.query.filter(StrConfig.key == key, StrConfig.child_id == child_id).first()
        if not dbconf:
            dbconf = StrConfig(key=key, value=value, child_id=child_id)
            db.session.add(dbconf)
        else:
            old_v = dbconf.value
    dbconf.value = value
    error(f"changing {key} from {old_v} to {value}")
    Events.config_changed.notify(conf=dbconf, old_value=old_v)

    if child_id == 0 and key.hide_in_virtual_child():
        for child in Child.query.filter(Child.mode == ChildMode.virtual, Child.id != 0).all():
            set_hconfig(key, value, child.id)

    if commit:
        db.session.commit()


@cache.cache(ttl=500,)
def get_hconfigs(child_id: int = None, json=False):
    if child_id == None:
        child_id = hutils.current_child_id()

    return {**{f'{u.key}' if json else u.key: u.value for u in BoolConfig.query.filter(BoolConfig.child_id == child_id).all()},
            **{f'{u.key}' if json else u.key: u.value for u in StrConfig.query.filter(StrConfig.child_id == child_id).all()},
            # ConfigEnum.telegram_fakedomain:hdomain(DomainType.telegram_faketls),
            # ConfigEnum.ssfaketls_fakedomain:hdomain(DomainType.ss_faketls),
            # ConfigEnum.fake_cdn_domain:hdomain(DomainType.fake_cdn)
            }


def get_hconfigs_childs(child_ids: list[int], json=False):
    if len(child_ids) == 0:
        child_ids = [c.id for c in Child.query.all()]
    return {c: get_hconfigs(c, json) for c in child_ids}


def add_or_update_config(commit: bool = True, child_id: int = None, override_unique_id: bool = True, **config):
    if child_id == None:
        child_id = hutils.current_child_id()
    c = config['key']
    ckey = ConfigEnum(c)
    if c == ConfigEnum.unique_id and not override_unique_id:
        return

    v = str(config['value']).lower() == "true" if ckey.type() == bool else config['value']
    if ckey in [ConfigEnum.db_version]:
        return
    set_hconfig(ckey, v, child_id, commit=commit)


def bulk_register_configs(hconfigs, commit: bool = True, override_child_id: int = None, override_unique_id: bool = True):
    from hiddifypanel.panel import hiddify
    for conf in hconfigs:
        # print(conf)
        if conf['key'] == ConfigEnum.unique_id and not override_unique_id:
            continue
        child_id = override_child_id if override_child_id is not None else hiddify.get_child(conf.get('child_unique_id', None))
        # print(conf, child_id, conf.get('child_unique_id', None), override_child_id)
        add_or_update_config(commit=False, child_id=child_id, **conf)
    if commit:
        db.session.commit()
