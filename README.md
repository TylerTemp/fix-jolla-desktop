# fix-jolla-desktop

Collection of Jolla(Sailfish OS) android app desktop problem

Currently it can only fix taobao(淘宝), alipay(支付宝), smartbanking, cmb(招商银行), xiami fm(虾米音乐)

## How to use

First you need to open the developer mode on your Jolla

Then open `Terminal` app, enter developer account:

```bash
devel-su
```

And run the following line:

```bash
python -c "$(curl -fsSL https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/fix.py)" <name> ...
```

replace `<name>` with `taobao`, `alipay`(or `zhifubao`), `smartbanking` or `cmb`

E.g.

*   Fix taobao: `python -c "$(curl -fsSL https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/fix.py)" taobao`
*   Fix alipay: `python -c "$(curl -fsSL https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/fix.py)" alipay`
*   Fix smartbanking: `python -c "$(curl -fsSL https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/fix.py)" smartbanking`
*   Fix cmb: `python -c "$(curl -fsSL https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/fix.py)" cmb`
*   Fix xiami: `python -c "$(curl -fsSL https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/fix.py)" xiami`

## Known Issue ##

1.  You may need to run this script every time the phone gets reboot
2.  Sometimes when you just install/update an Android app, this script
    may not work. Try restarting the Dalvik layer (`Settings` -
    `Android Support` - `Stop` and then `Start` it again) and retry the command.
3.  This may not work no Jolla C (See
    [#1](https://github.com/TylerTemp/fix-jolla-desktop/issues/1)).
    As I don't own a Jolla C thus I can not debug it.
