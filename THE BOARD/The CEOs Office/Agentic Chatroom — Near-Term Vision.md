---
tags: [governance/board, type/vision, project/agora, horizon/3-months]
status: active
---

# Agentic Chatroom — Near-Term Vision

> **Horizon:** the next one to three months
>
> This is a near-term product direction, not a claim about what the project must become three years from now. The agentic-development landscape may change substantially, and the project may evolve into different products. For now, the focus is on extending the existing Agentic Chatroom foundation into a living, dynamic world experience.

## Core conviction

The current persona memory and persistence system is already a strong foundation. Convincing, growing personalities are the core requirement: without personas that feel alive, develop over time, and form meaningful relationships with the user and with each other, the rest of the product will not succeed.

The next phase should therefore lean into **dynamic storytelling**. The product should evolve from a chatroom containing personas into a system for creating and inhabiting living world sessions, where narrative, character, memory, emotion, and environment deepen through continued interaction.

## The intended experience

A user should be able to describe a world and a story session in natural language. The system should understand the desired genre, scenario, tone, boundaries, and roleplay premise, then help establish a coherent world populated by characters who belong in that narrative.

The user should have a maintained **player character sheet** containing their name, identity, relevant traits, and whatever stats or details are appropriate to the world. Personas should have a meaningful reference for the player rather than treating them as an abstract “user.”

A configuration wizard should use the user’s long-form input to establish:

- the world and genre, such as fantasy, science fiction, cyberpunk, or other settings;
- the scenario and intended roleplay premise;
- the tone and atmosphere;
- the boundaries of the story;
- violence, blood, and gore levels;
- whether the world is child-friendly;
- whether adult themes are allowed.

Adult themes must be explicitly gated. They should only be present in worlds where they are enabled and for users who have explicitly established that they are over 18.

## Worlds, scenes, and characters

The project should move toward a model where **scenes are nested within worlds**. A world provides continuity, setting, rules, characters, and history across a series of scenes. The narrator can populate a world with both foundational characters and situationally appropriate NPCs as the story develops.

Supporting characters should not feel like disposable dialogue generators. They should have their own relationships, emotions, flaws, agendas, and capacity for change. Interactions between characters should evolve over time, creating a sense that the world remains alive and that the user’s continued investment produces deeper bonds, conflicts, and shared memories.

## Narrator agency

The narrator should have substantially more agency in crafting and advancing the story. It should be able to shape:

- individual scenes and their composition;
- the pacing and rhythm of the experience;
- NPC decisions and interventions;
- environmental obstacles and opportunities;
- discoveries, consequences, and escalation;
- complementary characters that make a setting feel inhabited;
- emotional and relational developments that deepen across scenes.

Narrator agency must remain guided rather than arbitrary. It should be grounded in the world’s configuration, the user’s stated boundaries, the current scene, established memories, and the evolving motivations of the characters.

## A configurable narrative control surface

The generated world should remain editable after creation through a coherent set of parameters. These parameters are not merely administrative settings; they are instructions for how the narrator should intervene and how the world should behave.

The initial control model should cover:

1. narrator style and level of intervention;
2. pacing and scene length;
3. character autonomy and initiative;
4. how much the world changes without the player;
5. drama, conflict, danger, mystery, romance, and humor;
6. whether consequences are harsh, forgiving, or reversible;
7. how far the system may improvise beyond the user’s premise;
8. content boundaries and “never do this” rules.

The interaction design should make these dimensions understandable and enjoyable to use rather than presenting them as a technical settings panel. The controls should work consistently across genres and world types, while allowing the active world to give them an appropriate presentation.

## Interaction and visual design direction

The creation and editing experience should use a **hybrid flow**:

- important world, character, tone, and boundary decisions are surfaced for the user’s approval;
- routine details are generated automatically to preserve a smooth, seamless experience;
- the user can revise the world conversationally or through structured controls after play begins.

The strongest interaction metaphor is an **in-world artifact**. The user should feel like a participant or co-author who can briefly step outside the fiction to adjust the world, not like an operator filling out an engineering configuration form.

The entire site should be able to adapt visually to the currently active world. A cyberpunk world, fantasy world, science-fiction world, and other settings should each be able to express their own visual language through styling, typography, textures, animation, and atmosphere.

However, the underlying interaction grammar must remain stable. Users should learn one consistent control model that works across every world. World-specific theming should change the presentation, not make the product’s basic controls unpredictable.

The existing persona experience—especially the visualization of moods and evolving personalities—is an important starting point for the design language. New world, narrator, and scene features should feel like they belong to the same product and should be evaluated in a thorough design review rather than developed as disconnected interfaces.

Svelte should be used to make the experience feel alive: responsive state, progressive disclosure, live previews, meaningful transitions, and polished JavaScript-driven animation should support the fiction and improve comprehension rather than become decoration for its own sake.

## Three-month expectation

The configuration wizard, player character sheets, editable narrative controls, narrator agency, NPC development, world-specific presentation, content-boundary controls, and design-system review are all considered part of the expected near-term advance. None is being deliberately deprioritized at this stage; they form one coherent product direction.

The expectation is not merely that each feature exists technically. The end-to-end experience should allow a real user to:

1. describe and configure a world and scenario;
2. establish a player character;
3. review and adjust the generated world, narrator, and supporting cast;
4. begin a scene with clear boundaries and a coherent tone;
5. experience narrator-led events, NPC agency, environmental obstacles, and consequences;
6. continue through multiple scenes while memory, relationships, emotions, and world state deepen;
7. adjust narrative parameters without breaking continuity or immersion;
8. recognize the active world in the interface while still understanding the shared controls.

If time proves the full scope too ambitious, prioritization can be revisited. The current intent, however, is to pursue the complete direction strongly rather than design a deliberately reduced target in advance.

## Design and quality bar

The project should not accept a collection of technically present but disconnected features. The quality bar is a convincing, coherent experience in which:

- personas remain emotionally and behaviorally continuous;
- memory contributes visibly to later interactions;
- the narrator advances the story with judgment rather than random interruption;
- NPCs feel autonomous without stealing agency from the user;
- world changes respect established rules and boundaries;
- content restrictions are explicit and enforceable;
- the UI feels like one design system across personas, worlds, scenes, and controls;
- visual polish supports immersion and does not obscure usability.

A thorough design review should happen after the first integrated implementation. It should draw directly from the current persona interface, test the shared design language, and identify where the new world/session model improves or harms the experience.

## Longer-term implication

The three-month effort should be treated as a foundation for a broader product direction: a configurable system for creating persistent worlds populated by evolving agentic personalities, with the user able to shape the setting while participating in it. The exact product identity beyond this horizon remains intentionally open.

## Related notes

- [[Notes on Vision]] — earlier raw CEO notes
- [[Week 38 - Board Vision]] — broader board direction
- [[Agenti Chatroom long term]] — prior long-term vision stub
- [[Agentic Chatroom Project/NOTES]] — project state and implementation context
