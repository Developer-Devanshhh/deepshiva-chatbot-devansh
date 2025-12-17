import { NextRequest, NextResponse } from 'next/server';

const API_URL = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

// DELETE /api/documents/[docId] - Delete a document
export async function DELETE(
  request: NextRequest,
  context: { params: Promise<{ docId: string }> }
) {
  try {
    const token = request.headers.get('authorization');
    const { docId } = await context.params;
    
    const response = await fetch(`${API_URL}/documents/${docId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': token || '',
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': 'true',
      },
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Document delete proxy error:', error);
    return NextResponse.json(
      { detail: 'Failed to delete document' },
      { status: 500 }
    );
  }
}
