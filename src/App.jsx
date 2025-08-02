import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>I Love my India 🇮🇳🇮🇳🇮🇳</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count} 🥳 
        </button>
        <p>Hello divyansh modi here</p>
        <p>I am pursuing computer engineering</p>
        <p>I love exploring different domains</p>
        <p>I like videogaphy</p>
        <p>nature is very beautiful</p>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more this is the new version 2.0
      </p>
    </>
  )
}

export default App
