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
  formErrors: ErrorValues
}
