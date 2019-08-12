export interface ErrorValues {
  general: string
  verificationCode: string
}

export interface VerificationFormProps {
  submitValidation: Function
  formErrors: ErrorValues
  loading: boolean
}

export interface FormValues {
  verificationCode: string
}
