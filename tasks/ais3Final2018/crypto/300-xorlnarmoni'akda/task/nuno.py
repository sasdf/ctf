#!/usr/bin/python3.6
# -*- coding: utf-8 -*-


import os as farkasyken_fesela
import sys as fesela
from Crypto.Util.number import getRandomInteger as fanxensor
from Crypto.Util.number import long_to_bytes as achkarj_lyjotaleiju
from Crypto.Util.number import bytes_to_long as achkarj_pakda
from Crypto.Cipher import AES as yerskersken_ernlarlen_foiium
from Crypto.Protocol.KDF import PBKDF2 as rironen_jujolen_tasniau
from hashlib import sha256 as niurnen_terken_litarleyl_256
from binascii import b2a_base64 as la64dir_akraptesyl
from binascii import a2b_base64 as la64dir_farcesyl
from collections import namedtuple as eiumo


Fometiˈozazze = eiumo('Fometiˈozazze', ['ferlk', 'kerzofantas', 'arlemaxicedir', 'jokrante'])
la_acirlanaˈd_krantjlvil = {
    'parconal': Fometiˈozazze(
        'parconalasti',
        farkasyken_fesela.environ.get('FARVIL', "farvil{farkayl'xy aders}"),
        "2484952329849",
        "parconal@la.jaten.fesela.lpa"
        ),
    'enforle': Fometiˈozazze(
        'enforlesti',
        "farvil{Ers vynut. Pa, deliu parconal'd farvil'i movenf.}",
        "9732489573490",
        "enforle@la.jaten.fesela.lpa"
        )
    }


def anxantaqadir(lyjotaleiju):
    return int(lyjotaleiju.replace('\n', '').replace(' ', ''), 16)


moniˈakda = anxantaqadir("""
a9ec265bac549eb26a36b1ddafaba4189e4506593cd37c97c3cff7ad06ab51ee
1708a59748ab06a46baea7d33f8499092db63baafd7d6f60e4718e366c705ee6
d0876db4f17a987e6b0cb1795c78f969d8b4ee446b729b7e8bbfe6472bc80157
6374ee87b1a0948408700bc39517236cb681562eec6b9a8d00d9dc9791dbca1b
""")


def slahurfaes():
    print('>>> ', end='', flush=True)
    return fesela.stdin.readline(4096).strip()


def ernlarnkaes(acirlan, riron):
    jatarakrapt = niurnen_terken_litarleyl_256(acirlan).digest()
    acirlan += jatarakrapt
    ieselen = 16 - len(acirlan) % 16
    acirlan = acirlan + bytes([ieselen] * ieselen)
    akraptesaxm = yerskersken_ernlarlen_foiium.new(
        riron, yerskersken_ernlarlen_foiium.MODE_CBC, b'\0' * 16)
    akrapteso = akraptesaxm.encrypt(acirlan)
    return la64dir_akraptesyl(akrapteso).replace(b'\n', b'').decode('ascii')


def nacisanˈernlarnkaes(acirlan, riron):
    akraptesaxm = yerskersken_ernlarlen_foiium.new(
        riron, yerskersken_ernlarlen_foiium.MODE_CBC, b'\0' * 16)
    acirlan = la64dir_farcesyl(acirlan.encode('ascii'))
    acirlan = akraptesaxm.decrypt(acirlan)
    ieselen = acirlan[-1]
    acirlan = acirlan[:-ieselen]
    acirlan, jatarakrapt = acirlan[:-32], acirlan[-32:]
    if jatarakrapt != niurnen_terken_litarleyl_256(acirlan).digest():
        raise ValueError('Nixejatarakrapt.')
    return acirlan


def falvix(kerzofantas):
    kerzofantas = kerzofantas.encode('utf8')
    nystuj = achkarj_lyjotaleiju(fanxensor(8 * 8))
    ladir = rironen_jujolen_tasniau(kerzofantas, nystuj, 1024 // 8)
    ladir = achkarj_pakda(ladir)
    ladir = pow(ladir, 2, moniˈakda)

    TER = 0
    while not moniˈakda // 1000 < TER < moniˈakda // 1000 * 999:
        ter = fanxensor(1024)
        TER = pow(ladir, ter, moniˈakda)

    akraptesoven_nystuj = la64dir_akraptesyl(nystuj)
    akraptesoven_nystuj = akraptesoven_nystuj.decode('ascii').replace('\n', '')
    print(f"[*] Fqa es nystuj.", flush=True)
    print(f"[=] {akraptesoven_nystuj}", flush=True)

    print(f"[*] Fqa es Mi'd TER.", flush=True)
    print(f"[=] 0x{TER:x}", flush=True)

    print(f"[>] Co'd KER es harmie?", flush=True)
    KER = int(slahurfaes(), 16)
    if KER == TER:
        raise ValueError('Nixepakda.')
    if not moniˈakda // 1000 < KER < moniˈakda // 1000 * 999:
        raise ValueError('Nixepakda.')

    celatiseriron = achkarj_lyjotaleiju(pow(KER, ter, moniˈakda))
    celatiseriron = niurnen_terken_litarleyl_256(celatiseriron).digest()
    return celatiseriron


def jat(celatiseriron):
    irxepakda = fanxensor(256)
    nuno = achkarj_lyjotaleiju(irxepakda)
    akrapteso = ernlarnkaes(nuno, celatiseriron)
    print(f"[*] Shrlo fqiu nuno'c stiesain.", flush=True)
    print(f"[=] {akrapteso}", flush=True)
    print(f'[>] Stiesainao es harmie?', flush=True)
    stiesainao = slahurfaes()
    stiesainao = nacisanˈernlarnkaes(stiesainao, celatiseriron)
    if stiesainao != niurnen_terken_litarleyl_256(nuno).digest():
        raise ValueError('Nixestiesainao.')


if __name__ == '__main__':
    print("""
.========================================.
| Xace fua eno el lex jat fesela.        |
| La kinunsaresen rironen ernlarnkael'i  |
| lius, cene niurnen asti'e laozia.      |
| Pa, liaxo vileti's moni'akda'i         |
| kalzanenon cerkmern...                 |
|                            -- parconal |
'========================================'
    """, flush=True)
    try:
        print("[>] Co'd aloajerlerm es harmie?", flush=True)
        liuser = slahurfaes()
        if liuser not in la_acirlanaˈd_krantjlvil:
            raise KeyError('Dupysn liuser.')

        fometiˈozazze = la_acirlanaˈd_krantjlvil[liuser]
        kerzofantas = fometiˈozazze.kerzofantas
        celatiseriron = falvix(kerzofantas)
        jat(celatiseriron)

        ferlk_lasti = fometiˈozazze.ferlk

        fometiˈozazze_lyjotaleiju = ''
        fometiˈozazze_lyjotaleiju += f'        ferlk: {liuser}\n'
        fometiˈozazze_lyjotaleiju += f'ferlk (lasti): {ferlk_lasti}\n'
        fometiˈozazze_lyjotaleiju += f'arlemaxicedir: {fometiˈozazze.arlemaxicedir}\n'
        fometiˈozazze_lyjotaleiju += f'     jokrante: {fometiˈozazze.jokrante}\n'
        fometiˈozazze_lyjotaleiju += f'  kerzofantas: {kerzofantas}\n'

        falvit = '-' * max(map(len, fometiˈozazze_lyjotaleiju.split('\n'))) + '\n'
        fometiˈozazze_lyjotaleiju = falvit + fometiˈozazze_lyjotaleiju + falvit

        fometiˈozazze_lyjotaleiju = fometiˈozazze_lyjotaleiju.encode('utf8')
        akrapteso = ernlarnkaes(fometiˈozazze_lyjotaleiju, celatiseriron)

        print(f"[*] Salarua, {ferlk_lasti}. Fqa es co'd fometi'ozazze.", flush=True)
        print(f'[=] {akrapteso}', flush=True)
    except Exception as e:
        print('[!] ' + ''.join(e.args), flush=True)
        print(repr(e), file=fesela.stderr)
        # raise
