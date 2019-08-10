import { useState, SyntheticEvent } from 'react'
import { FormValues } from './types'

const useVerificationForm = (callback: Function) => {
  const defaultProps = {
    verificationCode: '',
  }

  const [formValues, setFormValues] = useState<FormValues>(defaultProps)

  const handleSubmit = (event: SyntheticEvent) => {
    if (event) {
      event.preventDefault()
    }
    callback()
  }

  const handleFormValues = (event: any) => {
    event.persist()
    setFormValues(formValues => ({ ...formValues, [event.target.name]: event.target.value }))
  }

  return {
    handleSubmit,
    handleFormValues,
    formValues,
  }
}

export default useVerificationForm
