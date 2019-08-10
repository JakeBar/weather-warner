export interface ErrorValues {
  general: string
  name: string
  phone_number: string
  postal_code: string
}

export interface SignUpFormProps {
  submitDetails: Function
  formErrors: ErrorValues
}

export interface FormValues {
  name: string
  postal_code: string
  phone_number: string
}
