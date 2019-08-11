import { useState, SyntheticEvent } from 'react'
import { FormValues } from './types'

const useSignUpForm = (callback: Function) => {
  const defaultProps = {
    name: '',
    phone_number: '',
    postal_code: '',
  }

  const [formValues, setFormValues] = useState<FormValues>(defaultProps)

  const handleSubmit = (event: SyntheticEvent) => {
    if (event) {
      event.preventDefault()
    }
    callback()
  }

  // @ts-ignore
  const handleFormValues = event => {
    event.persist()
    setFormValues(values => ({ ...values, [event.target.name]: event.target.value }))
  }

  return {
    handleSubmit,
    handleFormValues,
    formValues,
  }
}

export default useSignUpForm
