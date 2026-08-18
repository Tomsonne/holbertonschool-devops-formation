# Merge Conflict Resolution

The conflict occurred on the `version` line because both branches modified the same line with different values. The `feature/scale-up` branch set the version to `1.1.0`, while the `feature/dark-mode` branch set it to `2.0.0`.

Git merged the `replicas` and `feature_dark_mode` lines automatically because the branches changed different lines. I resolved the conflict by keeping `version: 2.0.0`, while also preserving `replicas: 4` and `feature_dark_mode: true`.