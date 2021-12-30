import hooks from "@misago/hooks"
import DemoWarning from "./DemoWarning"

const register = () => {
  hooks.THREADS_ALL_TOP.push(DemoWarning)
}

export default register