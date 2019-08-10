import React, { useEffect, useState } from 'react'
import { Header, Divider, Transition } from 'semantic-ui-react'

const SignUpSuccess = () => {
  const [visibility, setVisiblity] = useState(false)

  useEffect(() => {
    setVisiblity(true)
  }, [])

  return (
    <Transition visible={visibility} duration={800}>
      <div>
        <Divider hidden />
        <Header style={{ color: 'white' }} as="h2" textAlign="center">
          You&apos;ve successfully signed up!
        </Header>
      </div>
    </Transition>
  )
}

export default SignUpSuccess
