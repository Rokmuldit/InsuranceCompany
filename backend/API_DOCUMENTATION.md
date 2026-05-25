# Документація API Страхової Компанії

Цей документ містить детальний опис усіх ендпоінтів бекенд-системи страхової компанії.

---

## Загальні ендпоінти

### `GET /`
- **Опис:** Вітальне повідомлення та перевірка зв'язку з базою даних.
- **Відповідь:** `{"message": "Welcome to the Insurance Company API on MSSQL"}`

### `GET /health`
- **Опис:** Перевірка стану системи та підключення до БД.
- **Відповідь:** `{"status": "ok", "database": "connected"}`

---

## 1. Тарифні плани (`/paid-plans`)
Управління тарифними планами страхування.

### `POST /paid-plans/`
- **Опис:** Створити новий тарифний план.
- **Вхідні дані (`PaidPlanCreate`):**
  - `name`: string (max 50) - Назва.
  - `description`: string | null - Опис.
  - `payment_amount`: decimal - Сума оплати.
  - `payment_period`: string (max 50) - Період оплати.
- **Відповідь (`PaidPlanResponse`):** Об'єкт тарифного плану з `id`.

### `GET /paid-plans/`
- **Опис:** Отримати список усіх тарифних планів.
- **Відповідь:** `list[PaidPlanResponse]`

### `GET /paid-plans/{plan_id}`
- **Опис:** Отримати тарифний план за ID.
- **Відповідь:** `PaidPlanResponse`

### `PUT /paid-plans/{plan_id}`
- **Опис:** Оновити існуючий тарифний план.
- **Вхідні дані (`PaidPlanUpdate`):** Ті самі поля, що й при створенні.
- **Відповідь:** `PaidPlanResponse`

### `DELETE /paid-plans/{plan_id}`
- **Опис:** Видалити тарифний план.
- **Статус:** 204 No Content.

---

## 2. Договори страхування (`/insurance-contracts`)
Управління договорами між клієнтами та компанією.

### `POST /insurance-contracts/`
- **Опис:** Створити новий договір страхування.
- **Вхідні дані (`InsuranceContractCreate`):**
  - `plan_id`: UUID
  - `client_id`: UUID
  - `agent_id`: UUID
- **Відповідь (`InsuranceContractResponse`):** Детальна інформація про договір, включаючи дані клієнта та агента.

### `GET /insurance-contracts/`
- **Опис:** Отримати всі договори страхування.
- **Відповідь:** `list[InsuranceContractResponse]`

### `GET /insurance-contracts/not-active`
- **Опис:** Отримати всі неактивні договори.
- **Відповідь:** `list[InsuranceContractResponse]`

### `GET /insurance-contracts/{contract_id}`
- **Опис:** Отримати договір за ID.
- **Відповідь:** `InsuranceContractResponse`

### `GET /insurance-contracts/client/{client_id}`
- **Опис:** Отримати договори конкретного клієнта.
- **Відповідь:** `list[InsuranceContractResponse]`

### `GET /insurance-contracts/agent/{agent_id}`
- **Опис:** Отримати договори конкретного агента.
- **Відповідь:** `list[InsuranceContractResponse]`

### `GET /insurance-contracts/plan/{plan_id}`
- **Опис:** Отримати договори за конкретним тарифним планом.
- **Відповідь:** `list[InsuranceContractResponse]`

### `PATCH /insurance-contracts/{contract_id}/activate`
- **Опис:** Активувати договір (встановлює дату початку/завершення та статус `is_active=True`).
- **Відповідь:** `InsuranceContractResponse`

### `DELETE /insurance-contracts/{contract_id}`
- **Опис:** Видалити договір.
- **Статус:** 204 No Content.

---

## 3. Страхові події (`/insurance-events`)
Реєстрація та обробка подій, що можуть бути страховими випадками.

### `POST /insurance-events/contract/{contract_id}`
- **Опис:** Зареєструвати страхову подію для договору.
- **Вхідні дані (`InsuranceEventCreate`):**
  - `event_date`: date
  - `description`: string | null
- **Відповідь (`InsuranceEventResponse`):** Об'єкт події з `id`.

### `GET /insurance-events/contract/{contract_id}`
- **Опис:** Отримати всі події за ID договору.
- **Відповідь:** `list[InsuranceEventResponse]`

### `GET /insurance-events/{event_id}`
- **Опис:** Отримати подію за ID.
- **Відповідь:** `InsuranceEventResponse`

### `PATCH /insurance-events/{event_id}/status`
- **Опис:** Визначити, чи є подія страховим випадком.
- **Вхідні дані (`InsuranceEventStatusUpdate`):**
  - `is_insurance_case`: boolean
- **Відповідь (`InsuranceEventResponse`)**

### `DELETE /insurance-events/{event_id}`
- **Опис:** Видалити подію.
- **Статус:** 204 No Content.

---

## 4. Страхові виплати (`/insurance-payments`)
Фіксація виплат за страховими випадками.

### `POST /insurance-payments/`
- **Опис:** Зареєструвати страхову виплату.
- **Вхідні дані (`InsurancePaymentCreate`):**
  - `contract_id`: UUID
  - `event_id`: UUID
  - `payment_date`: date
  - `payment_amount`: decimal
- **Відповідь (`InsurancePaymentResponse`):** Об'єкт виплати з `id`.

### `GET /insurance-payments/`
- **Опис:** Отримати всі страхові виплати.
- **Відповідь:** `list[InsurancePaymentResponse]`

### `DELETE /insurance-payments/{payment_id}`
- **Опис:** Видалити виплату.
- **Статус:** 204 No Content.

---

## 5. Персональні дані (`/personal-data`)
Управління анкетами клієнтів та агентів (ПІБ, телефон, адреса).

### `POST /personal-data/`
- **Опис:** Створити персональні дані та адресу.
- **Вхідні дані (`PersonalDataCreate`):** ПІБ, дата народження, телефон + дані адреси (регіон, місто, вулиця, будинок, квартира).
- **Відповідь (`PersonalDataResponse`)**

### `GET /personal-data/`
- **Опис:** Отримати список усіх анкет персональних даних.
- **Відповідь:** `list[PersonalDataResponse]`

### `GET /personal-data/client/{client_id}`
- **Опис:** Отримати анкету за ID клієнта.
- **Відповідь:** `PersonalDataResponse`

### `GET /personal-data/{pd_id}`
- **Опис:** Отримати анкету за її ID.
- **Відповідь:** `PersonalDataResponse`

### `PATCH /personal-data/{pd_id}`
- **Опис:** Частково оновити дані анкети або адресу.
- **Вхідні дані (`PersonalDataUpdate`):** Усі поля необов'язкові.
- **Відповідь (`PersonalDataResponse`)**

### `DELETE /personal-data/{pd_id}`
- **Опис:** Видалити анкету та пов'язану адресу.
- **Статус:** 204 No Content.

---

## 6. Клієнти (`/clients`)
Клієнти страхової компанії (суб'єкти, що мають персональні дані).

### `POST /clients/`
- **Опис:** Створити клієнта.
- **Вхідні дані (`ClientCreate`):**
  - `personal_data_id`: UUID
- **Відповідь (`ClientResponse`):** Об'єкт клієнта, розгорнутий з персональними даними та адресою.

### `POST /clients/search`
- **Опис:** Складний пошук клієнтів за ПІБ, телефоном або датою народження.
- **Вхідні дані (`ClientSearch`):** Поля для фільтрації.
- **Відповідь:** `list[ClientResponse]`

### `GET /clients/`
- **Опис:** Отримати всіх клієнтів.
- **Відповідь:** `list[ClientResponse]`

### `GET /clients/{client_id}`
- **Опис:** Отримати клієнта за ID.
- **Відповідь:** `ClientResponse`

### `DELETE /clients/{client_id}`
- **Опис:** Видалити клієнта.
- **Статус:** 204 No Content.

---

## 7. Агенти (`/agents`)
Агенти страхової компанії (клієнти, що виконують роль агентів).

### `POST /agents/`
- **Опис:** Створити агента.
- **Вхідні дані (`AgentCreate`):**
  - `client_id`: UUID
- **Відповідь (`AgentResponse`):** Об'єкт агента, розгорнутий з персональними даними та адресою.

### `POST /agents/search`
- **Опис:** Складний пошук агентів за ПІБ, телефоном або датою народження.
- **Вхідні дані (`AgentSearch`):** Поля для фільтрації.
- **Відповідь:** `list[AgentResponse]`

### `GET /agents/`
- **Опис:** Отримати всіх агентів.
- **Відповідь:** `list[AgentResponse]`

### `GET /agents/{agent_id}`
- **Опис:** Отримати агента за ID.
- **Відповідь:** `AgentResponse`

### `DELETE /agents/{agent_id}`
- **Опис:** Видалити агента.
- **Статус:** 204 No Content.
