package preview

import "os"

import (
	"context"
)

type Preview struct {
	ctx context.Context
	dir string
}

func NewPreview(ctx context.Context, dir string) Preview {
	return Preview{
		ctx: ctx,
		dir: dir,
	}
}

func (p Preview) FileBytes() ([]byte, error) {
	stat, err := os.Stat(p.dir)
	if err != nil {
		return nil, err
	}

	data, err := os.ReadFile(p.dir)
	if err != nil {
		return nil, err
	}

	if stat.Size() == 0 {
		null := "empty"
		data = []byte(null)
	}

	return data, nil
}
