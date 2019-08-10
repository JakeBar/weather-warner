export interface ErrorValues {
  general: string
  verification_code: string
}

export interface VerificationFormProps {
  phoneNumber: string
  submitValidation: Function
  formErrors: ErrorValues
}

export interface FormValues {
  verificationCode: string
}
