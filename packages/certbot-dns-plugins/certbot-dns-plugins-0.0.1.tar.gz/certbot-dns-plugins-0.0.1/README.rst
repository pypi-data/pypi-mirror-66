Certbot DNS Plugin for DNSPod
================================


安装
------

.. code-block:: sh

    pip install certbot-dns-plugins

配置文件
==========

假如文件路径如下:

~/.secrets/certbot/dnspod.ini

内容::

    certbot_dns_plugins:dnspod_token_id = <token id>
    certbot_dns_plugins:dnspod_token = <token>

chmod::

    chmod 600 ~/.secrets/certbot/dnspod.ini


创建证书::

    sudo certbot certonly \
    -a certbot-dns-plugins:dnspod \
    --certbot-dns-plugins:dnspod-credentials ~/.secrets/certbot/dnspod.ini \
    -d example.com

自动续期(可以放到crontab中执行)::

    certbot renew --deploy-hook "service nginx reload"

crontab(每周一的1:01分执行)::

    1 1 * * 1 certbot renew --deploy-hook "service nginx reload"

其他
=========

`怎样编写一个certbot插件 <https://certbot.eff.org/docs/contributing.html#writing-your-own-plugin>`_

官方插件：
https://certbot.eff.org/docs/using.html#dns-plugins

其他第三方插件:
https://certbot.eff.org/docs/using.html#third-party-plugins

官方插件是参数形式是::

 --dns-cloudflare-credentials

而第三方插件的参数是::

    --authenticator certbot-dns-plugins:dnspod

或者::

    -a certbot-dns-plugins:dnspod
