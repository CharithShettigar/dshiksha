from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', 'main.urls', name='www'),
    host(r'erp', 'dshiksha_erp.urls', name='erp'),
    host(r'school', 'school.urls', name='school'),
)