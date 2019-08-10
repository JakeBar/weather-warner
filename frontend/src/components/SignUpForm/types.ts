import { ErrorValues } from '../FormContainer/types'

export interface SignUpFormProps {
  submitDetails: Function
  formErrors: ErrorValues
}

export interface FormValues {
  name: string
  postal_code: string
  phone_number: string
}
