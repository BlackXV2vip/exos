export * as PublicEventManifest from "./public-event-manifest"

import { Event } from "@exos-agent-ai/schema/event"
import { EventManifest } from "@exos-agent-ai/schema/event-manifest"

export const Definitions = EventManifest.ServerDefinitions
export const Latest = Event.latest(Definitions)
