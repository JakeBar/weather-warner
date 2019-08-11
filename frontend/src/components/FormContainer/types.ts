export interface ErrorValues {
  general: string
  name: string
  phone_number: string
  postcode: string
  verification_code: string
}

export interface ApplicationState {
  submitted: boolean
  verified: boolean
  formErrors: ErrorValues
}
