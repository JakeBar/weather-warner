export interface ErrorValues {
  general: string
  name: string
  phone_number: string
  postcode: string
}

export interface SignUpFormProps {
  submitDetails: Function
  formErrors: ErrorValues
}

export interface FormValues {
  name: string
  postcode: string
  phone_number: string
}
