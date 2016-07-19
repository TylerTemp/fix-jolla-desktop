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
python -c "$(curl -fsSL https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/fix.py)" <name>
```

replace `<name>` with `taobao`, `alipay`(or `zhifubao`), `smartbanking` or `cmb`

E.g.

*   Fix taobao: `python -c "$(curl -fsSL https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/fix.py)" taobao`
*   Fix alipay: `python -c "$(curl -fsSL https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/fix.py)" alipay`
*   Fix smartbanking: `python -c "$(curl -fsSL https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/fix.py)" smartbanking`
*   Fix cmb: `python -c "$(curl -fsSL https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/fix.py)" cmb`
*   Fix xiami: `python -c "$(curl -fsSL https://raw.githubusercontent.com/TylerTemp/fix-jolla-desktop/master/fix.py)" xiami`
