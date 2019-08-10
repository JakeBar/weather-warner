/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable jsx-a11y/label-has-associated-control */
import React from 'react'
import { Segment, Form } from 'semantic-ui-react'
import useVerificationForm from './hooks'
import { VerificationFormProps } from './types'

const VerificationForm = (props: VerificationFormProps) => {
  const verifyDetails = () => {
    const { phoneNumber } = props
    props.submitValidation(phoneNumber, formValues)
  }

  const { formValues, handleFormValues, handleSubmit } = useVerificationForm(verifyDetails)

  const { error } = props

  const verificationError = error ? { error } : {}

  return (
    <Form error={error ? error.length > 0 : false} size="large" onSubmit={handleSubmit}>
      <Segment style={{ backgroundColor: 'transparent', border: 'none', boxShadow: 'none' }}>
        <Form.Field>
          <label style={{ color: 'white' }}>Verification Code</label>
          <Form.Input
            {...verificationError}
            name="verificationCode"
            type="text"
            required
            onChange={handleFormValues}
            value={formValues.verificationCode}
          />
        </Form.Field>

        <Form.Button
          style={{ border: '1px solid white', backgroundColor: 'transparent', color: 'white' }}
          fluid
          size="large"
          type="submit"
        >
          Verify Code
        </Form.Button>
      </Segment>
    </Form>
  )
}

export default VerificationForm
