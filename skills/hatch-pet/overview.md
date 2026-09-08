## Overview

Create a Codex-compatible v2 animated pet from a concept, brand cue, company/prospect name, one or more reference images, or any combination of those inputs. Every newly hatched pet is an 8x11 atlas with the 9 standard animation rows plus 16 clockwise look directions and is packaged with `spriteVersionNumber: 2`. The intermediate 8x9 atlas exists only to assemble and review rows 0-8; never package it as a new pet.

User-facing inputs are optional. If the user omits a pet name, infer one from the concept, brand, company, or reference filenames; if that is not possible, choose a short friendly name. If the user omits a description, infer one from the concept or references. If the user omits reference images, generate the base pet from text first, then use that base as the canonical reference for every animation row.
