export interface ErrorValues {
  general: string
  verification_code: string
}

export interface VerificationFormProps {
  submitValidation: Function
  formErrors: ErrorValues
}

export interface FormValues {
  verificationCode: string
}
