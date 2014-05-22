from platform import linux_distribution

if 'Ubuntu' or 'Debian' in linux_distribution():
    base_lib_path = "/usr/lib"
else:
    base_lib_path = "/usr/libexec"

pacemaker_binaries = "/usr/sbin/"
corosync_binaries = "/usr/sbin/"
corosync_conf_file = "/etc/corosync/corosync.conf"
cluster_conf_file = "/etc/cluster/cluster.conf"
fence_agent_binaries = "/usr/sbin/"
pengine_binary = base_lib_path + "/pacemaker/pengine"
crmd_binary = base_lib_path + "/pacemaker/crmd"
stonithd_binary = base_lib_path + "/pacemaker/stonithd"
pcs_version = "0.9.115"
crm_report = pacemaker_binaries + "crm_report"
crm_verify = pacemaker_binaries + "crm_verify"
pcsd_cert_location = "/var/lib/pcsd/pcsd.crt"
pcsd_key_location = "/var/lib/pcsd/pcsd.key"
corosync_uidgid_dir = "/etc/corosync/uidgid.d/"
