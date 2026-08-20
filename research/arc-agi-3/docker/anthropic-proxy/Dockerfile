FROM alpine:3.20
RUN apk add --no-cache squid \
    && mkdir -p /var/cache/squid /var/log/squid /run/squid \
    && chown -R squid:squid /var/cache/squid /var/log/squid /run/squid
RUN printf '%s\n' \
    'http_port 3128' \
    '' \
    'acl allowed_host dstdomain .anthropic.com .claude.ai' \
    'acl allowed_port port 443' \
    'acl connect_method method CONNECT' \
    '' \
    'http_access allow connect_method allowed_host allowed_port' \
    'http_access deny all' \
    '' \
    'access_log none' \
    'cache_log /var/log/squid/cache.log' \
    'cache deny all' \
    'coredump_dir /var/cache/squid' \
    'pid_filename none' \
    > /etc/squid/squid.conf
EXPOSE 3128
CMD ["squid", "-N", "-f", "/etc/squid/squid.conf"]
