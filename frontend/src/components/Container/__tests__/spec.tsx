import React from 'react'
import { shallow } from 'enzyme'
import Container from '../index'

describe('ContainerPage', () => {
  describe('component', () => {
    it('Renders simple component', () => {
      const wrapper = shallow(<Container />)
      expect(wrapper.find('Fragment')).toHaveLength(1)
    })
  })
})
