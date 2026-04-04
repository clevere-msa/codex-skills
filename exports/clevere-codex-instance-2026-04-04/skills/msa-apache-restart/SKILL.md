---
name: msa-apache-restart
description: Restart Apache httpd in the MSA environment (titan/shell/msa_apache) using /usr/local/bin/bounce-apache.sh, including pre-restart config validation and post-restart verification. Use when asked to bounce/restart Apache, apply mod_perl changes, or reload vhost configuration.
---

# Msa Apache Restart

## Overview

Restart Apache safely in MSA environments after config or mod_perl changes. Follow a short pre-check, bounce, and verify workflow.

## Workflow

1. Validate config with the deployed config path:
   - `apachectl -f <dest>/apache2.conf -t`
   - Use the active deployed directory (not the repo copy).
2. Restart Apache using the standard wrapper:
   - `/usr/local/bin/bounce-apache.sh`
3. Verify service health:
   - Re-hit the target URL (e.g., `/cgi-bin/entrance.cgi`)
   - Check the vhost error log for new errors.
