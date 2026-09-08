## Quick Decision Trees

### "Which framework should I use?"

```
Which framework?
├─ I want full control, maximum performance, no framework overhead
│  └─ core/ (imperative API)
├─ I know React, want familiar component patterns
│  └─ react/ (React reconciler)
├─ I want fine-grained reactivity, optimal re-renders
│  └─ solid/ (Solid reconciler)
└─ I'm building a library/framework on top of OpenTUI
   └─ core/ (imperative API)
```

### "I need to display content"

```
Display content?
├─ Plain or styled text -> components/text-display.md
├─ Container with borders/background -> components/containers.md
├─ Scrollable content area -> components/containers.md (scrollbox)
├─ ASCII art banner/title -> components/text-display.md (ascii-font)
├─ Code with syntax highlighting -> components/code-diff.md
├─ Diff viewer (unified/split) -> components/code-diff.md
├─ Line numbers with diagnostics -> components/code-diff.md
└─ Markdown content (streaming) -> components/code-diff.md (markdown)
```

### "I need user input"

```
User input?
├─ Single-line text field -> components/inputs.md (input)
├─ Multi-line text editor -> components/inputs.md (textarea)
├─ Select from a list (vertical) -> components/inputs.md (select)
├─ Tab-based selection (horizontal) -> components/inputs.md (tab-select)
└─ Custom keyboard shortcuts -> keyboard/REFERENCE.md
```

### "I need layout/positioning"

```
Layout?
├─ Flexbox-style layouts (row, column, wrap) -> layout/REFERENCE.md
├─ Absolute positioning -> layout/patterns.md
├─ Responsive to terminal size -> layout/patterns.md
├─ Centering content -> layout/patterns.md
└─ Complex nested layouts -> layout/patterns.md
```

### "I need animations"

```
Animations?
├─ Timeline-based animations -> animation/REFERENCE.md
├─ Easing functions -> animation/REFERENCE.md
├─ Property transitions -> animation/REFERENCE.md
└─ Looping animations -> animation/REFERENCE.md
```

### "I need to handle input"

```
Input handling?
├─ Keyboard events (keypress, release) -> keyboard/REFERENCE.md
├─ Focus management -> keyboard/REFERENCE.md
├─ Paste events -> keyboard/REFERENCE.md
├─ Mouse events -> components/containers.md
└─ Text selection -> components/text-display.md
```

### "I need to test my TUI"

```
Testing?
├─ Snapshot testing -> testing/REFERENCE.md
├─ Interaction testing -> testing/REFERENCE.md
├─ Test renderer setup -> testing/REFERENCE.md
└─ Debugging tests -> testing/REFERENCE.md
```

### "I need to debug/troubleshoot"

```
Troubleshooting?
├─ Runtime errors, crashes -> <framework>/gotchas.md
├─ Layout issues -> layout/REFERENCE.md + layout/patterns.md
├─ Input/focus issues -> keyboard/REFERENCE.md
└─ Repro + regression tests -> testing/REFERENCE.md
```

### Troubleshooting Index

- Terminal cleanup, crashes -> `core/gotchas.md`
- Text styling not applying -> `components/text-display.md`
- Input focus/shortcuts -> `keyboard/REFERENCE.md`
- Layout misalignment -> `layout/REFERENCE.md`
- Flaky snapshots -> `testing/REFERENCE.md`

For component naming differences and text modifiers, see `components/REFERENCE.md`.
