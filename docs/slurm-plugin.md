# SLURM Plugin

:::{note}

This has not yet been implemented.

:::

A possible implementation could be based on the [LUA Burst Buffer](https://slurm.schedmd.com/burst_buffer.html#lua_config) implementation (see [example](https://github.com/SchedMD/slurm/blob/master/etc/burst_buffer.lua.example)).

- `slurm_bb_setup`: initialize TRS system, capture system information
- `slurm_bb_data_in`: stage data to separate file space
- `slurm_bb_pre_run`: run first TRO record of base state of the file space
- `slurm_bb_post_run`:  run second TRO record at end of the job, amend TRO with additional process information
- `slurm_bb_data_out`: copy any changed files and the TRO back

