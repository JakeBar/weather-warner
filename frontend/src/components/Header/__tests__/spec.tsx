import React from 'react'
import { shallow } from 'enzyme'
import AppHeader from '../index'

describe('AppHeader', () => {
  describe('component', () => {
    it('Renders AppHeader component', () => {
      const wrapper = shallow(<AppHeader />)
      expect(wrapper.find('Header')).toHaveLength(1)
    })
  })
})
