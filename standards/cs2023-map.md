# CS2023 Map (ACM/IEEE-CS/AAAI Computer Science Curricula 2023)

> Standards map consumed by `tools/coverage.py`. One `##` section per Knowledge Area (17, final endorsed version, early 2024). Topic ids use the repo's 12 tracks. GIT/HCI full coverage deferred to v2 (placeholder ids in `frontiers`). Note: the draft-era KA "Logic and Computation" was merged into "Mathematical and Statistical Foundations" in the final version.

## Artificial Intelligence (AI)

- `ai-ml/search` — search, heuristics, adversarial search
- `ai-ml/knowledge-representation` — knowledge representation and reasoning, logical and probabilistic
- `ai-ml/machine-learning` — supervised and unsupervised learning, evaluation
- `ai-ml/planning` — planning and scheduling
- `ai-ml/agents` — agents and cognitive systems
- `ai-ml/natural-language-processing` — NLP, language understanding and generation
- `ai-ml/computer-vision` — perception and computer vision
- `ai-ml/robotics` — robotics, perception-action loops

## Algorithmic Foundations (AL)

- `cs-foundations/algorithms` — asymptotic analysis, design strategies, fundamental algorithms
- `cs-foundations/automata` — automata theory, formal languages, computability
- `cs-foundations/complexity` — complexity classes, P vs NP, reductions
- `cs-foundations/distributed-algorithms` — distributed algorithms, consensus, fault tolerance

## Architecture and Organization (AR)

- `hardware/digital-systems` — digital logic, combinational and sequential systems
- `hardware/machine-organization` — machine-level data representation, assembly-level organization
- `hardware/memory-organization` — memory hierarchy, cache, virtual memory
- `hardware/io-interfacing` — interfacing and communication, I/O systems
- `hardware/multiprocessing` — multiprocessing, alternative architectures, performance enhancement

## Data Management (DM)

- `data/data-modeling` — conceptual and relational modeling, schemas
- `data/relational-databases` — relational model, database design
- `data/query-languages` — SQL, query languages, views
- `data/transaction-processing` — transactions, concurrency control, recovery
- `data/physical-design` — storage, indexing, physical database design
- `data/information-retrieval` — information storage and retrieval, search
- `data/distributed-databases` — distributed and parallel databases, big data systems

## Foundations of Programming Languages (FPL)

- `programming/programming-paradigms` — paradigms: imperative, OO, functional, logic, concurrent
- `programming/type-systems` — types, type checking, polymorphism
- `programming/program-semantics` — language semantics, correctness, abstract machines
- `programming/language-translation` — parsing, interpretation, compilation, linking
- `programming/runtime-systems` — runtime organization, memory management, garbage collection

## Graphics and Interactive Techniques (GIT)

> Full KA coverage deferred to v2; key topics mapped to `frontiers` as placeholders.

- `frontiers/graphics-rendering` — rendering pipeline, rasterization, ray tracing
- `frontiers/graphics-modeling` — 3D geometry, curves and surfaces, modeling
- `frontiers/interactive-techniques` — interaction techniques, animation, VR/AR

## Human-Computer Interaction (HCI)

> Full KA coverage deferred to v2; key topics mapped to `frontiers` as placeholders.

- `frontiers/ux-design` — user-centered design, usability engineering
- `frontiers/accessibility` — accessibility and inclusive design
- `frontiers/hci-evaluation` — evaluation methods, user studies

## Mathematical and Statistical Foundations (MSF)

- `cs-foundations/discrete-structures` — sets, relations, functions, combinatorics, proof
- `cs-foundations/logic` — propositional and predicate logic, proof systems
- `cs-foundations/graph-theory` — graphs, trees, graph algorithms
- `cs-foundations/probability-statistics` — probability, distributions, statistics, hypothesis testing
- `cs-foundations/linear-algebra` — vectors, matrices, linear transformations

## Networking and Communication (NC)

- `systems-software/networking` — layered models, protocols, addressing, routing
- `systems-software/internet-applications` — DNS, HTTP, web and client-server computing
- `systems-software/wireless-mobile` — wireless and mobile networking

## Operating Systems (OS)

- `systems-software/os-principles` — roles, abstraction, structure, virtualization
- `systems-software/concurrency` — threads, synchronization, deadlock
- `systems-software/scheduling` — CPU scheduling and dispatch
- `systems-software/memory-management` — virtual memory, paging, allocation
- `systems-software/file-systems` — storage, file systems, protection
- `systems-software/device-management` — device management, drivers, interrupts

## Parallel and Distributed Computing (PDC)

- `systems-software/parallel-computing` — parallel decomposition, synchronization, Amdahl's law
- `systems-software/gpu-computing` — GPU and massive-parallel computing
- `systems-software/distributed-systems` — distributed architectures, failure handling, consensus
- `systems-software/cloud-computing` — virtualization, cloud service models

## Software Development Fundamentals (SDF)

- `programming/basic-constructs` — syntax, data types, control flow, functions, recursion
- `programming/data-structures` — fundamental data structures and algorithms
- `programming/development-methods` — refactoring, debugging, basic testing
- `programming/tooling` — build systems, version control, CI

## Software Engineering (SE)

- `architecture-design/requirements` — requirements engineering, elicitation, specifications
- `architecture-design/software-design` — design principles, design approaches, patterns
- `architecture-design/software-architecture` — architecture styles, quality attributes
- `quality-testing/software-quality` — verification and validation, quality assurance
- `quality-testing/software-testing` — test levels, test techniques, automation
- `engineering-process/process-models` — lifecycle models, agile, process improvement
- `engineering-process/project-management` — planning, estimation, risk, monitoring
- `operations/software-maintenance` — software evolution, maintenance, legacy systems

## Security (SEC)

- `security/security-foundations` — security mindset, threat modeling, risk analysis
- `security/cryptography` — symmetric and asymmetric crypto, hashing, key management
- `security/access-control` — authentication, authorization, identity
- `security/os-security` — operating system security, protection mechanisms
- `security/network-security` — network security, secure protocols
- `security/web-security` — web application security, injection, XSS
- `security/secure-coding` — secure coding practices, security testing
- `security/digital-forensics` — digital forensics, incident response

## Society, Ethics, and the Profession (SEP)

- `engineering-process/professional-ethics` — professional ethics, codes of conduct, ethical analysis
- `engineering-process/social-context` — computing and society, social impact
- `engineering-process/intellectual-property` — IP, copyright, patents, licensing
- `engineering-process/privacy-civil-liberties` — privacy and civil liberties
- `engineering-process/professional-communication` — professional communication and teamwork

## Systems Fundamentals (SF)

- `cs-foundations/systems-abstraction` — abstraction, layering, interfaces
- `cs-foundations/computational-paradigms` — system-level paradigms: event-driven, reactive, etc.
- `cs-foundations/state-machines` — state, state machines, invariants
- `cs-foundations/cross-layer-communication` — cross-layer communication and coordination

## Specialized Platform Development (SPD)

- `programming/web-platforms` — web platforms, frameworks, platform constraints
- `programming/mobile-platforms` — mobile platforms, app lifecycle, constraints
- `programming/game-platforms` — game development platforms
- `programming/industrial-platforms` — embedded and industrial platforms, IoT

## Sources

- CS2023 official knowledge model intro (17 KAs list, alphabetical by abbreviation): https://csed.acm.org/wp-content/uploads/2024/04/1.3-Introduction-to-Knowledge-Model.pdf
- CS2023 final report (ACM DL, DOI 10.1145/3664191): https://dl.acm.org/doi/10.1145/3664191
- Eaton et al., "Artificial Intelligence in the CS2023 Undergraduate Computer Science Curricula" (AAAI-24): https://ojs.aaai.org/index.php/AAAI/article/view/30352/32394
