package restbuilder

import "context"

type Resource interface {
	Get(context.Context, int) (Marshallable, error)
}

type Marshallable interface {
	JSON() ([]byte, error)
}
