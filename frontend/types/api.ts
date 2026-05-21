export interface Address {
  region: string;
  city: string;
  street: string;
  house: string;
  apartment?: string | null;
}

export interface PersonalData {
  id: string;
  first_name: string;
  last_name: string;
  middle_name?: string | null;
  birth_date: string;
  phone_number: string;
  address?: Address;
}

export interface PersonalDataCreate extends Omit<PersonalData, 'id'> {
  region: string;
  city: string;
  street: string;
  house: string;
  apartment?: string | null;
}

export interface PaidPlan {
  id: string;
  name: string;
  description?: string | null;
  payment_amount: number;
  payment_period: string;
}

export interface PaidPlanCreate {
  name: string;
  description?: string | null;
  payment_amount: number;
  payment_period: string;
}

export interface Client {
  id: string;
  personal_data_id: string;
  personal_data?: PersonalData;
}

export interface ClientCreate {
  personal_data_id: string;
}

export interface Agent {
  id: string;
  client_id: string;
  personal_data?: PersonalData;
}

export interface AgentCreate {
  client_id: string;
}

export interface InsuranceContract {
  id: string;
  plan_id: string;
  client_id: string;
  agent_id: string;
  start_date?: string | null;
  end_date?: string | null;
  is_active: boolean;
  plan?: PaidPlan;
  client?: Client;
  agent?: Agent;
}

export interface InsuranceContractCreate {
  plan_id: string;
  client_id: string;
  agent_id: string;
}

export interface InsuranceEvent {
  id: string;
  contract_id: string;
  event_date: string;
  description?: string | null;
  is_insurance_case: boolean;
}

export interface InsuranceEventCreate {
  event_date: string;
  description?: string | null;
}

export interface InsurancePayment {
  id: string;
  contract_id: string;
  event_id: string;
  payment_date: string;
  payment_amount: number;
}

export interface InsurancePaymentCreate {
  contract_id: string;
  event_id: string;
  payment_date: string;
  payment_amount: number;
}
