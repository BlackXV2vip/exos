import { run as runTui, type TuiInput } from "@exos-agent-ai/tui"
import { Global } from "@exos-agent-ai/core/global"
import { AppNodeBuilder } from "@exos-agent-ai/core/effect/app-node-builder"
import { Effect } from "effect"

export function run(input: TuiInput) {
  return runTui(input).pipe(Effect.provide(AppNodeBuilder.build(Global.node)))
}
