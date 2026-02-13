// State of the agent, make sure this aligns with your agent's state.
export type AgentState = {
  conversation_context: string[];
  total_token_count?: number;
  last_context_tokens?: number;
  last_response_tokens?: number;
  tokens_per_second?: number;
  proverbs?: string[];
}

// Person node schema from Neo4j
export type Person = {
  firstName?: string;
  lastName?: string;
  last_updated?: string;
  gender?: string;
  name?: string;
  exploration_depth?: number;
  is_complete?: boolean;
  relationship?: string;
  age?: number;
  email?: string;
}

// Available relationship types
export type RelationshipType =
  | "DAUGHTER_OF"
  | "PARENT_OF"
  | "BROTHER_OF"
  | "FATHER_OF"
  | "SON_OF"
  | "SPOUSE_OF"
  | "CHILD_OF"
  | "SIBLING_OF"
  | "WIFE_OF"
  | "MOTHER_OF"
  | "HUSBAND_OF";