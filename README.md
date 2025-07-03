# AutoGen Team State Migration (v0.4.x to v0.6.x)

Starting v0.4.9, the team state is using the agent name as the key instead of the agent ID, and the team_id field is removed from the state. This is to allow the state to be portable across different teams and runtimes. States saved with the old format may not be compatible with the new format in the future.

See `migrate_state.py` for the migration logic.

## Migration Test

Install `uv`:

```bash
curl -Ls https://install.uv.link | sh   # one-liner from the uv docs
```

How to run the migration test:

```bash
./setup_envs.sh
./run_migration_test.sh
```
