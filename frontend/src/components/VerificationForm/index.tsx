/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable jsx-a11y/label-has-associated-control */
import React, { useEffect, useState } from 'react'
import { Segment, Form, Transition, Message } from 'semantic-ui-react'
import useVerificationForm from './hooks'
import { VerificationFormProps } from './types'

const VerificationForm = (props: VerificationFormProps) => {
  const [visibility, setVisiblity] = useState(false)

  const verifyDetails = () => {
    // eslint-disable-next-line no-use-before-define, @typescript-eslint/no-use-before-define
    props.submitValidation(formValues)
  }

  const { formValues, handleFormValues, handleSubmit } = useVerificationForm(verifyDetails)

  const { formErrors } = props
  const verificationCodeErrors = formErrors.verification_code
    ? { error: formErrors.verification_code }
    : {}

  useEffect(() => {
    setVisiblity(true)
  }, [])

  return (
    <Transition visible={visibility} duration={800}>
      <Form error={formErrors.general.length > 0} size="large" onSubmit={handleSubmit}>
        <Segment style={{ backgroundColor: 'transparent', border: 'none', boxShadow: 'none' }}>
          <Form.Field>
            <label style={{ color: 'white' }}>Verification Code</label>
            <Form.Input
              {...verificationCodeErrors}
              name="verificationCode"
              type="text"
              required
              onChange={handleFormValues}
              value={formValues.verificationCode}
            />
          </Form.Field>

          {formErrors.general && <Message error content={formErrors.general} />}

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
    </Transition>
  )
}

export default VerificationForm
