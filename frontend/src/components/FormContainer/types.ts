// TODO change away from camelCase on frontend
export interface ErrorValues {
  general: string
  name: string
  phone_number: string
  postal_code: string
  verification_code: string
}

export interface ApplicationState {
  submitted: boolean
  verified: boolean
  phone_number: string
  formErrors: ErrorValues
}
