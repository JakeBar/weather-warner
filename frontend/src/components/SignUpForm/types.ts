export interface ErrorValues {
  general: string
  name: string
  phoneNumber: string
  postalCode: string
}

export interface SignUpFormProps {
  submitDetails: Function
  formErrors: ErrorValues
}

export interface FormValues {
  name: string
  postalCode: string
  phoneNumber: string
}
