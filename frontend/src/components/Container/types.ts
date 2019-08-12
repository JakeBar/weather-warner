export interface ErrorValues {
  general: string
  name: string
  phoneNumber: string
  postalCode: string
  verificationCode: string
}

export interface ApplicationState {
  submitted: boolean
  verified: boolean
  loading: boolean
  formErrors: ErrorValues
}
