import React from "react"
import { Card, CardBody } from "@misago/UI/Card"

const TopPosters: React.FC = () => (
  <Card>
    <CardBody>
      <p>
        <strong>Note:</strong> This is a demo site. It's data is periodically wiped clean.
      </p>
      <p style={{ margin: "0px"}}>
        For feedback and discussions please use <a href="https://misago-project.org/c/misago-v4/25/">Misago v4 category on main forums</a>.
      </p>
    </CardBody>
  </Card>
)

export default TopPosters