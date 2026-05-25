export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface PersonalData {
  id: string;
  first_name: string;
  last_name: string;
  middle_name?: string | null;
  birth_date: string;
  phone_number: string;
  address_id: string;
  region: string;
  city: string;
  street: string;
  house: string;
  apartment?: string | null;
}

export interface PersonalDataCreate {
  first_name: string;
  last_name: string;
  middle_name?: string | null;
  birth_date: string;
  phone_number: string;
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
  first_name: string;
  last_name: string;
  middle_name?: string | null;
  birth_date: string;
  phone_number: string;
  address_id: string;
  region: string;
  city: string;
  street: string;
  house: string;
  apartment?: string | null;
}

export interface ClientCreate {
  personal_data_id: string;
}

export interface Agent {
  id: string;
  client_id: string;
  personal_data_id: string;
  first_name: string;
  last_name: string;
  middle_name?: string | null;
  birth_date: string;
  phone_number: string;
  address_id: string;
  region: string;
  city: string;
  street: string;
  house: string;
  apartment?: string | null;
}

export interface AgentCreate {
  client_id: string;
}

export interface InsuranceContract {
  contract_id: string;
  contract_amount: number;
  start_date: string;
  end_date: string;
  is_active: boolean;

  client_id: string;
  client_first_name: string;
  client_last_name: string;
  client_middle_name?: string | null;
  client_birth_date: string;
  client_phone_number: string;
  client_region: string;
  client_city: string;
  client_street: string;
  client_house: string;
  client_apartment?: string | null;

  agent_id: string;
  agent_first_name: string;
  agent_last_name: string;
  agent_middle_name?: string | null;
  agent_birth_date: string;
  agent_phone_number: string;
  agent_region: string;
  agent_city: string;
  agent_street: string;
  agent_house: string;
  agent_apartment?: string | null;
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
