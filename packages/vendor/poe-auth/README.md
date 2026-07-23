# exos-poe-auth

Poe authentication plugin for Exos Agent with browser-based OAuth and manual API key entry.

## Install

```bash
npm install exos-poe-auth
```

## Usage

Register the plugin with Exos Agent:

```ts
import { PoeAuthPlugin } from "exos-poe-auth";

const INTERNAL_PLUGINS = [
  PoeAuthPlugin
];
```

The plugin registers the `poe` auth provider and exposes two auth methods:

- `Login with Poe (browser)`
- `Manually enter API Key`

## Environment Variables

This package does not expose any environment variables.

## Config

This package does not expose any plugin-specific config options.
