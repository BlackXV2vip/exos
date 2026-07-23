import { AgentV2 } from "@exos-agent-ai/core/agent"
import { AISDK } from "@exos-agent-ai/core/aisdk"
import { Catalog } from "@exos-agent-ai/core/catalog"
import { CommandV2 } from "@exos-agent-ai/core/command"
import { Credential } from "@exos-agent-ai/core/credential"
import { AppNodeBuilder } from "@exos-agent-ai/core/effect/app-node-builder"
import { LayerNodePlatform } from "@exos-agent-ai/core/effect/app-node-platform"
import { LayerNode } from "@exos-agent-ai/core/effect/layer-node"
import { EventV2 } from "@exos-agent-ai/core/event"
import { FileSystem } from "@exos-agent-ai/core/filesystem"
import { FSUtil } from "@exos-agent-ai/core/fs-util"
import { Integration } from "@exos-agent-ai/core/integration"
import { Location } from "@exos-agent-ai/core/location"
import { Npm } from "@exos-agent-ai/core/npm"
import { PluginV2 } from "@exos-agent-ai/core/plugin"
import { Reference } from "@exos-agent-ai/core/reference"
import { SkillV2 } from "@exos-agent-ai/core/skill"
import { Effect, Layer } from "effect"
import { tempLocationLayer } from "../fixture/location"

const npmLayer = Layer.succeed(
  Npm.Service,
  Npm.Service.of({
    add: () => Effect.succeed({ directory: "", entrypoint: undefined }),
    install: () => Effect.void,
    which: () => Effect.succeed(undefined),
  }),
)

export const PluginTestLayer = AppNodeBuilder.build(
  LayerNode.group([
    FileSystem.node,
    FSUtil.node,
    Location.node,
    Npm.node,
    Credential.node,
    EventV2.node,
    LayerNodePlatform.httpClient,
    PluginV2.node,
    AgentV2.node,
    AISDK.node,
    Catalog.node,
    CommandV2.node,
    Integration.node,
    Reference.node,
    SkillV2.node,
  ]),
  [
    [Location.node, tempLocationLayer],
    [Npm.node, npmLayer],
  ],
)
