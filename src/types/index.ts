export type SupportedLanguage = 
  | 'rust' 
  | 'go' 
  | 'typescript' 
  | 'python' 
  | 'java' 
  | 'cpp' 
  | 'elixir';

export interface LanguageMeta {
  id: SupportedLanguage;
  name: string;
  category: string;
  typing: string;
  memory: string;
  concurrencyModel: string;
  color: string;
  badgeBg: string;
  extension: string;
  version: string;
}

export type ParadigmCategory = 
  | 'concurrency' 
  | 'memory' 
  | 'types' 
  | 'metaprogramming' 
  | 'functional' 
  | 'error_handling';

export interface CodeSnippet {
  language: SupportedLanguage;
  code: string;
  explanation: string;
  complexity: string;
  runtimeMechanics: string;
  keyConcepts: string[];
}

export interface ParadigmTopic {
  id: string;
  title: string;
  category: ParadigmCategory;
  tagline: string;
  theoreticalCore: string;
  architecturalTradeoffs: {
    pros: string[];
    cons: string[];
    bestFor: string;
  };
  implementations: Record<SupportedLanguage, CodeSnippet>;
}

// Memory Simulator Types
export interface MemoryBlock {
  id: string;
  label: string;
  type: 'stack' | 'heap';
  address: string;
  sizeBytes: number;
  value: string;
  color?: string;
  targetAddress?: string; // pointer target
  isBorrowed?: boolean;
  borrower?: string;
  isFreed?: boolean;
  refCount?: number;
}

export interface MemoryStackFrame {
  functionName: string;
  variables: MemoryBlock[];
}

export interface MemorySimStep {
  stepIndex: number;
  codeLine: number;
  actionTitle: string;
  explanation: string;
  stack: MemoryStackFrame[];
  heap: MemoryBlock[];
  highlightLines: number[];
  notes: string;
}

export interface MemorySimulationScenario {
  id: string;
  title: string;
  language: SupportedLanguage;
  description: string;
  code: string;
  steps: MemorySimStep[];
}

// Design Patterns Types
export interface PatternImplementation {
  language: SupportedLanguage;
  code: string;
  idiomaticNotes: string;
}

export interface PatternScenario {
  id: string;
  name: string;
  category: 'Structural' | 'Behavioral' | 'Concurrency' | 'Resilience';
  description: string;
  problemStatement: string;
  solutionArchitecture: string;
  diagramNodes: {
    id: string;
    label: string;
    role: string;
    status: 'idle' | 'active' | 'success' | 'warning' | 'error';
    x: number;
    y: number;
  }[];
  diagramEdges: {
    from: string;
    to: string;
    label: string;
    animated?: boolean;
  }[];
  interactiveActions: {
    id: string;
    label: string;
    description: string;
    icon: string;
  }[];
  implementations: Record<SupportedLanguage, PatternImplementation>;
}

// Benchmark & Radar Types
export interface ParadigmBenchmark {
  language: SupportedLanguage;
  coldStartupMs: number;
  memoryFootprintMb: number;
  concurrencyThroughputRps: number;
  latencyP99Ms: number;
  binarySizeMb: number;
  developerVelocityScore: number; // 1-10
  typeSafetyScore: number; // 1-10
}

export interface AlgorithmicComplexity {
  algorithm: string;
  paradigm: string;
  timeComplexityBest: string;
  timeComplexityAvg: string;
  timeComplexityWorst: string;
  spaceComplexity: string;
  cacheLocalityImpact: 'High' | 'Medium' | 'Low';
  allocationBehavior: string;
}

// Execution Runner Types
export interface ExecutionResult {
  stdout: string;
  stderr: string;
  exitCode: number;
  durationMs: number;
  isSimulated?: boolean;
  runtimeVersion?: string;
}
