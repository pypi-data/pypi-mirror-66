DNSPod Certbot DNS Plugin
=============================

`怎样编写一个certbot插件 <https://certbot.eff.org/docs/contributing.html#writing-your-own-plugin>`_

安装
------

.. code-block:: py

    pip install certbot-dns-plugins



使用参考别的插件：
https://certbot.eff.org/docs/using.html#dns-plugins


~/.secrets/certbot/dnspod.ini

certbot_dns_plugins:dnspod_token_id = 1
certbot_dns_plugins:dnspod_token = 2

执行：

    chmod 600 ~/.secrets/certbot/dnspod.ini

sudo certbot certonly \
  --certbot-dns-plugins:dnspod \
  --certbot-dns-plugins:dnspod-credentials ~/.secrets/certbot/dnspod.ini \
  --certbot-dns-plugins:dnspod-propagation-seconds 60 \
  --dry-run \
  -d example.com
