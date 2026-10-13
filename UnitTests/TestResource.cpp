/***************************************************************************
    Copyright (c) 2015 Philip Fortier

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
***************************************************************************/
#include "stdafx.h"
#include "CppUnitTest.h"
#include "View.h"
#include "ResourceEntity.h"
#include "ResourceMap.h"
#include "AppState.h"
#include "ResourceContainer.h"
#include "RasterOperations.h"
#include "format.h"
#include "Message.h"
#include "Text.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

// Defined in Message.cpp; not exposed in a header.
void MessageReadFrom(ResourceEntity &resource, sci::istream &byteStream, const std::map<BlobKey, uint32_t> &propertyBag);
void MessageWriteTo(const ResourceEntity &resource, sci::ostream &byteStream, std::map<BlobKey, uint32_t> &propertyBag);

std::wstring ToString(const RasterChangeHint& q)
{
    return fmt::format(L"RasterChangeHint:{0:08x}", (int)q);
}

namespace UnitTests
{		
    TEST_CLASS(TestResource)
    {
    public:
        TEST_CLASS_INITIALIZE(ClassSetup)
        {
        }

        TEST_CLASS_CLEANUP(ClassCleanup)
        {
        }

        TEST_METHOD(TestCreateDefaultResources)
        {
	        // Create the default resources.
            ResourceEntity *pTest = CreateDefaultViewResource(sciVersion0);
        }

        TEST_METHOD(TestViewMirror)
        {
            RasterChange change;
            ResourceEntity *pTest = CreateDefaultViewResource(sciVersion0);
            Assert::IsNotNull(pTest);
            RasterComponent *raster = pTest->TryGetComponent<RasterComponent>();
            Assert::IsNotNull(raster);
            // Insert second loop:
            change = InsertLoop(*raster, 0, false);
            Assert::AreEqual(change.hint, RasterChangeHint::NewView);
            // Make it a mirror of the first:
            change = MakeMirrorOf(*raster, 1, 0);
            Assert::AreEqual(change.hint, RasterChangeHint::NewView);
            Loop &loopOrig = raster->Loops[0];
            Assert::IsFalse(loopOrig.IsMirror);
            Assert::AreEqual(loopOrig.MirrorOf, (uint8_t)0xff);
            Loop &loopMirror = raster->Loops[1];
            Assert::IsTrue(loopMirror.IsMirror);
            Assert::AreEqual(loopMirror.MirrorOf, (uint8_t)0);
            // Un-mirror it
            change = MakeMirrorOf(*raster, 1, -1);
            Assert::AreEqual(change.hint, RasterChangeHint::NewView);
            Assert::IsTrue(!loopMirror.IsMirror);
            Assert::AreEqual(loopMirror.MirrorOf, (uint8_t)0xff);
        }

        TEST_METHOD(TestMessage3411RoundTrip)
        {
            // Two-entry version 0xD0C message (as in Laura Bow 2 floppy). The second entry's reference bytes are
            // leftover junk, which must survive a round trip unchanged.
            const uint8_t original[] =
            {
                0x0c, 0x0d, 0x00, 0x00, 0x1c, 0x00, 0x02, 0x00,
                0x01, 0x04, 0x00, 0x01, 0x63, 0x1c, 0x00, 0x7f, 0x20, 0x7f,
                0x11, 0x01, 0x01, 0x01, 0x63, 0x1f, 0x00, 0xa6, 0xa6, 0xa6,
                'H', 'i', 0x00,
                'Y', 'o', 0x00,
            };
            std::unique_ptr<ResourceEntity> resource(CreateMessageResource(sciVersion1_1));
            sci::istream in(original, (uint32_t)sizeof(original));
            std::map<BlobKey, uint32_t> propertyBag;
            MessageReadFrom(*resource, in, propertyBag);

            const TextComponent &text = resource->GetComponent<TextComponent>();
            Assert::IsTrue(text.Texts.size() == 2);
            Assert::AreEqual(std::string("Yo"), text.Texts[1].Text);

            sci::ostream out;
            MessageWriteTo(*resource, out, propertyBag);
            Assert::IsTrue(out.GetDataSize() == sizeof(original));
            Assert::IsTrue(0 == memcmp(original, out.GetInternalPointer(), sizeof(original)));
        }

	};
}