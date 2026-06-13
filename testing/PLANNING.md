
                           ┌──────────────────────────────┐
                           │ requirements for saving mode │
                           └───────────────────┬──────────┘
                                               │
                                               │
                                    ┌──────────┴────────────────────┐
                                    │ save a `save_state.json`      │
                                  ┌─│ in a `save_state_START_TIME/` ├──────────────► save x/y_axes, this_rounds_x/y_axes
                                  │ │ in a `save/` dir              ├─────────┐
                                  │ └──────────┬────────────────┬───┘         ▼
                                  │            │                │             comprehensively capture
                                  │            │                │             and save the session state
                                  ▼            │                └────────┐
                           save `start_time`   │                         │
                                               │                         │
                                               ▼                         ▼
                                        save `num_correct`,           allow the session to be resumed
                                        `num_incorrect`,              this requires rewriting `quiz()`
                                        `num_remaining` etc.          to take more general/generic parameters





















